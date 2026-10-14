"""Orders API endpoints."""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.deps import (
    get_current_user,
    get_restaurant_id_header,
    require_restaurant_access,
    resolve_tenant_id,
    user_has_permission,
)
from app.core.exceptions import ForbiddenError, NotFoundError
from app.db.session import get_db
from app.models.restaurant import Restaurant
from app.models.user import User
from app.schemas.common import PaginatedResponse
from app.schemas.order import (
    AssignRiderRequest,
    OrderCreate,
    OrderListItem,
    OrderOut,
    OrderStatusUpdate,
)
from app.services.order_service import OrderService

router = APIRouter(tags=["orders"])


def _tenant(user: User, header_id: Optional[UUID]) -> UUID:
    tenant = resolve_tenant_id(user, header_id)
    if not tenant:
        raise ForbiddenError("Restaurant context required")
    return tenant


@router.post("/public/{slug}/orders", response_model=OrderOut, status_code=201)
def place_public_order(slug: str, payload: OrderCreate, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.slug == slug).first()
    if not restaurant:
        raise NotFoundError("Restaurant not found")
    return OrderService(db).create_order(restaurant.id, payload, source="website")


@router.get("/public/orders/track/{order_number}", response_model=OrderOut)
def track_order(order_number: str, db: Session = Depends(get_db)):
    return OrderService(db).get_by_number(order_number)


@router.get("/orders", response_model=PaginatedResponse[OrderListItem])
def list_orders(
    status: Optional[str] = None,
    search: Optional[str] = Query(default=None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    user: User = Depends(require_restaurant_access),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    if not user_has_permission(user, "orders:*") and not user_has_permission(
        user, "orders:view"
    ):
        raise ForbiddenError("Missing orders permission")
    items, meta = OrderService(db).list_orders(
        _tenant(user, header_id), status=status, search=search, page=page, page_size=page_size
    )
    return PaginatedResponse(
        items=[OrderListItem.model_validate(i) for i in items], **meta
    )


@router.get("/orders/{order_id}", response_model=OrderOut)
def get_order(
    order_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(require_restaurant_access),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    if not user_has_permission(user, "orders:*") and not user_has_permission(
        user, "orders:view"
    ):
        raise ForbiddenError("Missing orders permission")
    return OrderService(db).get_order(_tenant(user, header_id), order_id)


@router.patch("/orders/{order_id}/status", response_model=OrderOut)
def update_order_status(
    order_id: UUID,
    payload: OrderStatusUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    if not user_has_permission(user, "orders:*") and not user_has_permission(
        user, "orders:update_status"
    ):
        raise ForbiddenError("Missing permission to update order status")
    return OrderService(db).update_status(
        _tenant(user, header_id), order_id, payload, changed_by_id=user.id
    )


@router.post("/orders/{order_id}/assign-rider", response_model=OrderOut)
def assign_rider(
    order_id: UUID,
    payload: AssignRiderRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    if not user_has_permission(user, "orders:*") and not user_has_permission(
        user, "orders:delivery"
    ):
        raise ForbiddenError("Missing permission to assign rider")
    return OrderService(db).assign_rider(
        _tenant(user, header_id), order_id, payload.rider_id
    )
