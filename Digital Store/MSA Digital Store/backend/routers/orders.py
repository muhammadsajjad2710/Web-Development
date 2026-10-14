from datetime import datetime
import time

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from database import get_db
from models import (
    Order,
    OrderItem,
    OrderStatus,
    Payment,
    PaymentStatus,
    DeliveryStatus,
    CartItem,
    Product,
    Inventory,
    User,
    UserRole,
    Customer,
    PaymentMethod,
)
from schemas import OrderCreate, OrderOut, OrderStatusUpdate, MessageOut
from auth import (
    get_current_user,
    get_optional_user,
    get_customer_profile,
    require_roles,
    get_password_hash,
)
from routers.products import compute_stock_status

router = APIRouter(prefix="/api/orders", tags=["Orders"])


def generate_order_number() -> str:
    return f"MSA-{int(time.time()) % 100000000:08d}"


def get_order_or_404(db: Session, order_id: int) -> Order:
    order = db.query(Order).options(joinedload(Order.items)).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def apply_status(db: Session, order: Order, new_status: OrderStatus) -> Order:
    order.status = new_status
    order.updated_at = datetime.utcnow()
    delivery = db.query(DeliveryStatus).filter(DeliveryStatus.order_id == order.id).first()
    if delivery:
        delivery.current_status = new_status
        delivery.updated_at = datetime.utcnow()

    if new_status in (OrderStatus.cancelled, OrderStatus.returned):
        for item in order.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if product:
                product.stock += item.quantity
                product.stock_status = compute_stock_status(product.stock)
                inv = db.query(Inventory).filter(Inventory.product_id == product.id).first()
                if inv:
                    inv.quantity = product.stock

    db.commit()
    db.refresh(order)
    return order


@router.post("", response_model=OrderOut, status_code=201)
def place_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    clear_cart = False

    if current_user and current_user.role == UserRole.customer:
        customer = get_customer_profile(current_user, db)
        cart_items = db.query(CartItem).filter(CartItem.customer_id == customer.id).all()
        source_items = [{"product_id": i.product_id, "quantity": i.quantity} for i in cart_items]
        clear_cart = True
        if not source_items and payload.guest_items:
            source_items = [{"product_id": i.product_id, "quantity": i.quantity} for i in payload.guest_items]
            clear_cart = False
    else:
        if not payload.guest_items:
            raise HTTPException(status_code=400, detail="Cart is empty. Add products or login.")
        source_items = [{"product_id": i.product_id, "quantity": i.quantity} for i in payload.guest_items]

        guest_email = (str(payload.email) if payload.email else f"guest_{payload.phone}@msa.local").lower()
        user = db.query(User).filter(User.email == guest_email).first()
        if not user:
            user = User(
                email=guest_email,
                phone=payload.phone,
                full_name=payload.customer_name,
                hashed_password=get_password_hash((payload.phone[-6:] if payload.phone else "guest1") or "guest1"),
                role=UserRole.customer,
            )
            db.add(user)
            db.flush()
            customer = Customer(
                user_id=user.id,
                address=payload.address,
                city=payload.city,
                district=payload.district,
            )
            db.add(customer)
            db.flush()
        else:
            customer = db.query(Customer).filter(Customer.user_id == user.id).first()
            if not customer:
                customer = Customer(
                    user_id=user.id,
                    address=payload.address,
                    city=payload.city,
                    district=payload.district,
                )
                db.add(customer)
                db.flush()

    if not source_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    line_items = []
    subtotal = 0.0
    for src in source_items:
        product = db.query(Product).filter(Product.id == src["product_id"], Product.is_active == True).first()  # noqa: E712
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {src['product_id']} not found")
        if product.stock < src["quantity"]:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name}")
        line_total = product.price * src["quantity"]
        subtotal += line_total
        line_items.append((product, src["quantity"], line_total))

    delivery = 0.0 if subtotal >= 5000 else 150.0
    total = subtotal + delivery

    order = Order(
        order_number=generate_order_number(),
        customer_id=customer.id,
        customer_name=payload.customer_name,
        phone=payload.phone,
        email=str(payload.email) if payload.email else None,
        address=payload.address,
        city=payload.city,
        district=payload.district,
        payment_method=payload.payment_method,
        status=OrderStatus.placed,
        subtotal=round(subtotal, 2),
        delivery_charges=delivery,
        total_amount=round(total, 2),
        notes=payload.notes,
    )
    db.add(order)
    db.flush()

    for product, qty, line_total in line_items:
        db.add(
            OrderItem(
                order_id=order.id,
                product_id=product.id,
                product_name=product.name,
                unit_price=product.price,
                quantity=qty,
                line_total=line_total,
                seller_id=product.seller_id,
            )
        )
        product.stock -= qty
        product.stock_status = compute_stock_status(product.stock)
        inv = db.query(Inventory).filter(Inventory.product_id == product.id).first()
        if inv:
            inv.quantity = product.stock

    db.add(
        Payment(
            order_id=order.id,
            method=payload.payment_method,
            status=PaymentStatus.pending,
            amount=total,
            reference=order.order_number,
        )
    )
    db.add(
        DeliveryStatus(
            order_id=order.id,
            current_status=OrderStatus.placed,
            courier_name="MSA Local Delivery",
        )
    )

    if clear_cart:
        db.query(CartItem).filter(CartItem.customer_id == customer.id).delete()

    db.commit()
    return get_order_or_404(db, order.id)


@router.get("", response_model=list[OrderOut])
def list_orders(
    status_filter: OrderStatus | None = Query(None, alias="status"),
    customer_id: int | None = None,
    seller_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Order).options(joinedload(Order.items))

    if current_user.role == UserRole.customer:
        customer = get_customer_profile(current_user, db)
        query = query.filter(Order.customer_id == customer.id)
    elif current_user.role == UserRole.seller:
        seller = current_user.seller
        if not seller:
            return []
        query = query.join(OrderItem).filter(OrderItem.seller_id == seller.id).distinct()
    elif current_user.role == UserRole.admin:
        if customer_id:
            query = query.filter(Order.customer_id == customer_id)
        if seller_id:
            query = query.join(OrderItem).filter(OrderItem.seller_id == seller_id).distinct()
    else:
        raise HTTPException(status_code=403, detail="Not allowed")

    if status_filter:
        query = query.filter(Order.status == status_filter)

    return query.order_by(Order.created_at.desc()).all()


@router.get("/track/{order_number}", response_model=OrderOut)
def track_order(order_number: str, db: Session = Depends(get_db)):
    order = (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(Order.order_number == order_number)
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get("/{order_id}", response_model=OrderOut)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = get_order_or_404(db, order_id)
    if current_user.role == UserRole.customer:
        customer = get_customer_profile(current_user, db)
        if order.customer_id != customer.id:
            raise HTTPException(status_code=403, detail="Not allowed")
    return order


@router.put("/{order_id}/status", response_model=OrderOut)
def update_order_status(
    order_id: int,
    payload: OrderStatusUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin, UserRole.seller)),
):
    order = get_order_or_404(db, order_id)
    return apply_status(db, order, payload.status)


@router.post("/{order_id}/cancel", response_model=OrderOut)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = get_order_or_404(db, order_id)
    if current_user.role == UserRole.customer:
        customer = get_customer_profile(current_user, db)
        if order.customer_id != customer.id:
            raise HTTPException(status_code=403, detail="Not allowed")
        if order.status not in (OrderStatus.placed, OrderStatus.confirmed):
            raise HTTPException(status_code=400, detail="Order can no longer be cancelled")
    elif current_user.role not in (UserRole.admin, UserRole.seller):
        raise HTTPException(status_code=403, detail="Not allowed")
    return apply_status(db, order, OrderStatus.cancelled)


@router.post("/{order_id}/return", response_model=OrderOut)
def return_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = get_order_or_404(db, order_id)
    if current_user.role == UserRole.customer:
        customer = get_customer_profile(current_user, db)
        if order.customer_id != customer.id:
            raise HTTPException(status_code=403, detail="Not allowed")
    if order.status != OrderStatus.delivered:
        raise HTTPException(status_code=400, detail="Only delivered orders can be returned")
    return apply_status(db, order, OrderStatus.returned)
