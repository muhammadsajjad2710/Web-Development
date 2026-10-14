"""Dashboard analytics service."""

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Any, Dict, List
from uuid import UUID

from sqlalchemy import Date, cast, func
from sqlalchemy.orm import Session

from app.core.enums import OrderStatus
from app.models.customer import Customer
from app.models.order import Order, OrderItem
from app.schemas import DashboardStats


class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def get_stats(self, restaurant_id: UUID) -> DashboardStats:
        now = datetime.now(timezone.utc)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        base = self.db.query(Order).filter(
            Order.restaurant_id == restaurant_id, Order.is_deleted.is_(False)
        )

        total_orders = base.count()
        today_orders = base.filter(Order.created_at >= today_start).count()
        pending_orders = base.filter(Order.status == OrderStatus.PENDING.value).count()
        completed_orders = base.filter(
            Order.status.in_(
                [OrderStatus.COMPLETED.value, OrderStatus.DELIVERED.value]
            )
        ).count()
        cancelled_orders = base.filter(
            Order.status.in_([OrderStatus.CANCELLED.value, OrderStatus.REJECTED.value])
        ).count()

        revenue_q = self.db.query(func.coalesce(func.sum(Order.total_amount), 0)).filter(
            Order.restaurant_id == restaurant_id,
            Order.is_deleted.is_(False),
            Order.status.notin_(
                [OrderStatus.CANCELLED.value, OrderStatus.REJECTED.value]
            ),
        )
        total_revenue = Decimal(str(revenue_q.scalar() or 0))
        today_revenue = Decimal(
            str(
                revenue_q.filter(Order.created_at >= today_start).scalar() or 0
            )
        )

        customer_count = (
            self.db.query(Customer)
            .filter(Customer.restaurant_id == restaurant_id, Customer.is_deleted.is_(False))
            .count()
        )
        repeat_customers = (
            self.db.query(Customer)
            .filter(
                Customer.restaurant_id == restaurant_id,
                Customer.is_deleted.is_(False),
                Customer.total_orders > 1,
            )
            .count()
        )

        return DashboardStats(
            total_orders=total_orders,
            today_orders=today_orders,
            pending_orders=pending_orders,
            completed_orders=completed_orders,
            cancelled_orders=cancelled_orders,
            total_revenue=total_revenue,
            today_revenue=today_revenue,
            customer_count=customer_count,
            repeat_customers=repeat_customers,
            top_selling_items=self._top_items(restaurant_id),
            recent_orders=self._recent_orders(restaurant_id),
            sales_by_day=self._sales_by_day(restaurant_id, days=7),
            orders_by_status=self._orders_by_status(restaurant_id),
        )

    def _top_items(self, restaurant_id: UUID, limit: int = 5) -> List[Dict[str, Any]]:
        rows = (
            self.db.query(
                OrderItem.item_name,
                func.sum(OrderItem.quantity).label("qty"),
                func.sum(OrderItem.total_price).label("revenue"),
            )
            .join(Order, Order.id == OrderItem.order_id)
            .filter(
                Order.restaurant_id == restaurant_id,
                Order.is_deleted.is_(False),
                Order.status.notin_(
                    [OrderStatus.CANCELLED.value, OrderStatus.REJECTED.value]
                ),
            )
            .group_by(OrderItem.item_name)
            .order_by(func.sum(OrderItem.quantity).desc())
            .limit(limit)
            .all()
        )
        return [
            {"name": r.item_name, "quantity": int(r.qty or 0), "revenue": float(r.revenue or 0)}
            for r in rows
        ]

    def _recent_orders(self, restaurant_id: UUID, limit: int = 8) -> List[Dict[str, Any]]:
        orders = (
            self.db.query(Order)
            .filter(Order.restaurant_id == restaurant_id, Order.is_deleted.is_(False))
            .order_by(Order.created_at.desc())
            .limit(limit)
            .all()
        )
        return [
            {
                "id": str(o.id),
                "order_number": o.order_number,
                "customer_name": o.customer_name,
                "status": o.status,
                "total_amount": float(o.total_amount),
                "currency": o.currency,
                "created_at": o.created_at.isoformat() if o.created_at else None,
            }
            for o in orders
        ]

    def _sales_by_day(self, restaurant_id: UUID, days: int = 7) -> List[Dict[str, Any]]:
        start = datetime.now(timezone.utc) - timedelta(days=days - 1)
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        rows = (
            self.db.query(
                cast(Order.created_at, Date).label("day"),
                func.coalesce(func.sum(Order.total_amount), 0).label("revenue"),
                func.count(Order.id).label("orders"),
            )
            .filter(
                Order.restaurant_id == restaurant_id,
                Order.is_deleted.is_(False),
                Order.created_at >= start,
                Order.status.notin_(
                    [OrderStatus.CANCELLED.value, OrderStatus.REJECTED.value]
                ),
            )
            .group_by(cast(Order.created_at, Date))
            .order_by(cast(Order.created_at, Date))
            .all()
        )
        by_day = {str(r.day): {"revenue": float(r.revenue), "orders": int(r.orders)} for r in rows}
        result = []
        for i in range(days):
            day = (start + timedelta(days=i)).date()
            key = str(day)
            entry = by_day.get(key, {"revenue": 0.0, "orders": 0})
            result.append({"date": key, **entry})
        return result

    def _orders_by_status(self, restaurant_id: UUID) -> List[Dict[str, Any]]:
        rows = (
            self.db.query(Order.status, func.count(Order.id))
            .filter(Order.restaurant_id == restaurant_id, Order.is_deleted.is_(False))
            .group_by(Order.status)
            .all()
        )
        return [{"status": status, "count": count} for status, count in rows]
