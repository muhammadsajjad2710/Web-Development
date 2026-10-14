from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from database import get_db
from models import (
    Order,
    OrderItem,
    OrderStatus,
    Product,
    Customer,
    Seller,
    SellerStatus,
    StockStatus,
    User,
    UserRole,
)
from schemas import DashboardStats, OrderOut, UserOut, MessageOut
from auth import require_roles

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/dashboard", response_model=DashboardStats)
def dashboard_stats(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin)),
):
    total_orders = db.query(func.count(Order.id)).scalar() or 0
    total_sales = (
        db.query(func.coalesce(func.sum(Order.total_amount), 0.0))
        .filter(Order.status.notin_([OrderStatus.cancelled]))
        .scalar()
        or 0.0
    )
    total_products = db.query(func.count(Product.id)).filter(Product.is_active == True).scalar() or 0  # noqa: E712
    total_customers = db.query(func.count(Customer.id)).scalar() or 0
    active_sellers = (
        db.query(func.count(Seller.id))
        .filter(Seller.status == SellerStatus.approved)
        .scalar()
        or 0
    )
    low_stock = (
        db.query(func.count(Product.id))
        .filter(Product.stock_status == StockStatus.low_stock, Product.is_active == True)  # noqa: E712
        .scalar()
        or 0
    )
    pending_orders = (
        db.query(func.count(Order.id))
        .filter(Order.status.in_([OrderStatus.placed, OrderStatus.confirmed]))
        .scalar()
        or 0
    )
    returned_orders = (
        db.query(func.count(Order.id)).filter(Order.status == OrderStatus.returned).scalar() or 0
    )

    recent = (
        db.query(Order)
        .options(joinedload(Order.items))
        .order_by(Order.created_at.desc())
        .limit(8)
        .all()
    )

    top = (
        db.query(
            OrderItem.product_id,
            OrderItem.product_name,
            func.sum(OrderItem.quantity).label("sold"),
            func.sum(OrderItem.line_total).label("revenue"),
        )
        .group_by(OrderItem.product_id, OrderItem.product_name)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(5)
        .all()
    )
    top_selling = [
        {"product_id": r.product_id, "name": r.product_name, "sold": int(r.sold or 0), "revenue": float(r.revenue or 0)}
        for r in top
    ]

    return DashboardStats(
        total_orders=total_orders,
        total_sales=float(total_sales),
        total_products=total_products,
        total_customers=total_customers,
        active_sellers=active_sellers,
        low_stock_products=low_stock,
        pending_orders=pending_orders,
        returned_orders=returned_orders,
        recent_orders=recent,
        top_selling_products=top_selling,
    )


@router.get("/customers", response_model=list[UserOut])
def list_customers(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin)),
):
    return db.query(User).filter(User.role == UserRole.customer).order_by(User.created_at.desc()).all()


@router.get("/health", response_model=MessageOut)
def admin_health(_: User = Depends(require_roles(UserRole.admin))):
    return {"message": "Admin API healthy"}
