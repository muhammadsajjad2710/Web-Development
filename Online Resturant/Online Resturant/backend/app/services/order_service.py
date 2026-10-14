"""Order lifecycle service."""

from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional, Tuple
from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from app.core.enums import OrderStatus
from app.core.exceptions import NotFoundError, ValidationAppError
from app.models.customer import Customer
from app.models.menu import MenuItem
from app.models.order import Order, OrderItem, OrderStatusHistory, Payment
from app.models.restaurant import Restaurant
from app.schemas.order import OrderCreate, OrderStatusUpdate
from app.utils.helpers import generate_order_number, paginate


class OrderService:
    def __init__(self, db: Session):
        self.db = db

    def list_orders(
        self,
        restaurant_id: UUID,
        status: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Tuple[List[Order], dict]:
        query = self.db.query(Order).filter(
            Order.restaurant_id == restaurant_id, Order.is_deleted.is_(False)
        )
        if status:
            query = query.filter(Order.status == status)
        if search:
            like = f"%{search}%"
            query = query.filter(
                (Order.order_number.ilike(like))
                | (Order.customer_name.ilike(like))
                | (Order.customer_phone.ilike(like))
            )
        total = query.count()
        items = (
            query.order_by(Order.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return items, paginate(total, page, page_size)

    def get_order(self, restaurant_id: UUID, order_id: UUID) -> Order:
        order = (
            self.db.query(Order)
            .options(joinedload(Order.items), joinedload(Order.status_history))
            .filter(
                Order.id == order_id,
                Order.restaurant_id == restaurant_id,
                Order.is_deleted.is_(False),
            )
            .first()
        )
        if not order:
            raise NotFoundError("Order not found")
        return order

    def get_by_number(self, order_number: str) -> Order:
        order = (
            self.db.query(Order)
            .options(joinedload(Order.items))
            .filter(Order.order_number == order_number, Order.is_deleted.is_(False))
            .first()
        )
        if not order:
            raise NotFoundError("Order not found")
        return order

    def create_order(
        self,
        restaurant_id: UUID,
        data: OrderCreate,
        source: str = "website",
        changed_by_id: Optional[UUID] = None,
    ) -> Order:
        restaurant = (
            self.db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        )
        if not restaurant:
            raise NotFoundError("Restaurant not found")

        if data.order_type == "delivery" and not data.delivery_address:
            raise ValidationAppError("Delivery address is required for delivery orders")

        customer = self._upsert_customer(restaurant_id, data)

        subtotal = Decimal("0.00")
        line_items: List[OrderItem] = []

        for line in data.items:
            menu_item = (
                self.db.query(MenuItem)
                .filter(
                    MenuItem.id == line.menu_item_id,
                    MenuItem.restaurant_id == restaurant_id,
                    MenuItem.is_deleted.is_(False),
                    MenuItem.is_available.is_(True),
                )
                .first()
            )
            if not menu_item:
                raise ValidationAppError(f"Menu item unavailable: {line.menu_item_id}")

            unit = menu_item.discount_price or menu_item.price
            if line.variation and "price_delta" in line.variation:
                unit += Decimal(str(line.variation["price_delta"]))
            if line.addons:
                for addon in line.addons:
                    unit += Decimal(str(addon.get("price", 0))) * Decimal(
                        str(addon.get("quantity", 1))
                    )

            total = unit * line.quantity
            subtotal += total
            line_items.append(
                OrderItem(
                    menu_item_id=menu_item.id,
                    item_name=menu_item.name,
                    quantity=line.quantity,
                    unit_price=unit,
                    total_price=total,
                    variation=line.variation,
                    addons=line.addons,
                    notes=line.notes,
                )
            )

        tax = (subtotal * (restaurant.tax_rate or Decimal("0")) / Decimal("100")).quantize(
            Decimal("0.01")
        )
        service = (
            subtotal * (restaurant.service_charge_rate or Decimal("0")) / Decimal("100")
        ).quantize(Decimal("0.01"))
        delivery_fee = Decimal("100.00") if data.order_type == "delivery" else Decimal("0.00")
        total_amount = subtotal + tax + service + delivery_fee

        order = Order(
            restaurant_id=restaurant_id,
            branch_id=data.branch_id,
            customer_id=customer.id if customer else None,
            order_number=generate_order_number(),
            order_type=data.order_type,
            status=OrderStatus.PENDING.value,
            payment_status="pending",
            payment_method=data.payment_method,
            customer_name=data.customer_name,
            customer_phone=data.customer_phone,
            customer_email=data.customer_email,
            delivery_address=data.delivery_address,
            special_instructions=data.special_instructions,
            subtotal=subtotal,
            tax_amount=tax,
            service_charge=service,
            delivery_fee=delivery_fee,
            discount_amount=Decimal("0.00"),
            total_amount=total_amount,
            currency=restaurant.currency or "PKR",
            source=source,
        )
        self.db.add(order)
        self.db.flush()

        for item in line_items:
            item.order_id = order.id
            self.db.add(item)

        self.db.add(
            OrderStatusHistory(
                order_id=order.id,
                from_status=None,
                to_status=OrderStatus.PENDING.value,
                changed_by_id=changed_by_id,
                note="Order placed",
            )
        )
        self.db.add(
            Payment(
                order_id=order.id,
                restaurant_id=restaurant_id,
                amount=total_amount,
                currency=order.currency,
                method=data.payment_method,
                status="pending",
            )
        )

        if customer:
            customer.total_orders = (customer.total_orders or 0) + 1
            customer.total_spent = (customer.total_spent or Decimal("0")) + total_amount
            customer.last_order_at = datetime.now(timezone.utc)

        self.db.commit()
        return self.get_order(restaurant_id, order.id)

    def update_status(
        self,
        restaurant_id: UUID,
        order_id: UUID,
        data: OrderStatusUpdate,
        changed_by_id: Optional[UUID] = None,
    ) -> Order:
        order = self.get_order(restaurant_id, order_id)
        try:
            new_status = OrderStatus(data.status)
        except ValueError as exc:
            raise ValidationAppError(f"Invalid order status: {data.status}") from exc

        old = order.status
        order.status = new_status.value
        if new_status in (OrderStatus.COMPLETED, OrderStatus.DELIVERED):
            order.completed_at = datetime.now(timezone.utc)
            order.payment_status = "paid"
        if new_status in (OrderStatus.CANCELLED, OrderStatus.REJECTED):
            order.cancelled_at = datetime.now(timezone.utc)
            order.cancellation_reason = data.note

        self.db.add(
            OrderStatusHistory(
                order_id=order.id,
                from_status=old,
                to_status=new_status.value,
                changed_by_id=changed_by_id,
                note=data.note,
            )
        )
        self.db.commit()
        return self.get_order(restaurant_id, order_id)

    def assign_rider(
        self, restaurant_id: UUID, order_id: UUID, rider_id: UUID
    ) -> Order:
        order = self.get_order(restaurant_id, order_id)
        order.assigned_rider_id = rider_id
        self.db.commit()
        return self.get_order(restaurant_id, order_id)

    def _upsert_customer(self, restaurant_id: UUID, data: OrderCreate) -> Optional[Customer]:
        customer = (
            self.db.query(Customer)
            .filter(
                Customer.restaurant_id == restaurant_id,
                Customer.phone == data.customer_phone,
                Customer.is_deleted.is_(False),
            )
            .first()
        )
        if customer:
            customer.full_name = data.customer_name
            if data.customer_email:
                customer.email = data.customer_email
            if data.delivery_address:
                customer.address = data.delivery_address
            return customer

        customer = Customer(
            restaurant_id=restaurant_id,
            full_name=data.customer_name,
            phone=data.customer_phone,
            email=data.customer_email,
            address=data.delivery_address,
        )
        self.db.add(customer)
        self.db.flush()
        return customer
