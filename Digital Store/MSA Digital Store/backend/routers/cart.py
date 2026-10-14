from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from database import get_db
from models import CartItem, Product, User, UserRole, StockStatus
from schemas import CartItemCreate, CartItemUpdate, CartOut, CartItemOut, MessageOut
from auth import get_current_user, get_customer_profile, require_roles

router = APIRouter(prefix="/api/cart", tags=["Cart"])

DELIVERY_FEE = 150.0
FREE_DELIVERY_THRESHOLD = 5000.0


def build_cart(db: Session, customer_id: int) -> dict:
    items = (
        db.query(CartItem)
        .options(joinedload(CartItem.product).joinedload(Product.images), joinedload(CartItem.product).joinedload(Product.category), joinedload(CartItem.product).joinedload(Product.seller))
        .filter(CartItem.customer_id == customer_id)
        .all()
    )
    subtotal = sum(i.product.price * i.quantity for i in items if i.product)
    delivery = 0.0 if subtotal == 0 or subtotal >= FREE_DELIVERY_THRESHOLD else DELIVERY_FEE
    return {
        "items": items,
        "subtotal": round(subtotal, 2),
        "delivery_charges": delivery,
        "total": round(subtotal + delivery, 2),
        "item_count": sum(i.quantity for i in items),
    }


@router.get("/me", response_model=CartOut)
def get_my_cart(
    current_user: User = Depends(require_roles(UserRole.customer)),
    db: Session = Depends(get_db),
):
    customer = get_customer_profile(current_user, db)
    return build_cart(db, customer.id)


@router.get("/{customer_id}", response_model=CartOut)
def get_cart(
    customer_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role == UserRole.customer:
        customer = get_customer_profile(current_user, db)
        if customer.id != customer_id:
            raise HTTPException(status_code=403, detail="Not allowed")
    elif current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not allowed")
    return build_cart(db, customer_id)


@router.post("/add", response_model=CartOut)
def add_to_cart(
    payload: CartItemCreate,
    current_user: User = Depends(require_roles(UserRole.customer)),
    db: Session = Depends(get_db),
):
    customer = get_customer_profile(current_user, db)
    product = db.query(Product).filter(Product.id == payload.product_id, Product.is_active == True).first()  # noqa: E712
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock_status == StockStatus.out_of_stock or product.stock < 1:
        raise HTTPException(status_code=400, detail="Product is out of stock")

    item = (
        db.query(CartItem)
        .filter(CartItem.customer_id == customer.id, CartItem.product_id == product.id)
        .first()
    )
    if item:
        item.quantity = min(item.quantity + payload.quantity, product.stock)
    else:
        item = CartItem(customer_id=customer.id, product_id=product.id, quantity=min(payload.quantity, product.stock))
        db.add(item)
    db.commit()
    return build_cart(db, customer.id)


@router.put("/item/{item_id}", response_model=CartOut)
def update_cart_item(
    item_id: int,
    payload: CartItemUpdate,
    current_user: User = Depends(require_roles(UserRole.customer)),
    db: Session = Depends(get_db),
):
    customer = get_customer_profile(current_user, db)
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.customer_id == customer.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    item.quantity = min(payload.quantity, item.product.stock or payload.quantity)
    db.commit()
    return build_cart(db, customer.id)


@router.delete("/item/{item_id}", response_model=CartOut)
def remove_cart_item(
    item_id: int,
    current_user: User = Depends(require_roles(UserRole.customer)),
    db: Session = Depends(get_db),
):
    customer = get_customer_profile(current_user, db)
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.customer_id == customer.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(item)
    db.commit()
    return build_cart(db, customer.id)


@router.delete("/clear", response_model=MessageOut)
def clear_cart(
    current_user: User = Depends(require_roles(UserRole.customer)),
    db: Session = Depends(get_db),
):
    customer = get_customer_profile(current_user, db)
    db.query(CartItem).filter(CartItem.customer_id == customer.id).delete()
    db.commit()
    return {"message": "Cart cleared"}
