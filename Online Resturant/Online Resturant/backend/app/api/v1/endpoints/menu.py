"""Menu API endpoints."""

from typing import List, Optional
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
from app.schemas.menu import (
    CategoryCreate,
    CategoryOut,
    CategoryUpdate,
    MenuItemCreate,
    MenuItemOut,
    MenuItemUpdate,
)
from app.services.menu_service import MenuService

router = APIRouter(tags=["menu"])


def _tenant(user: User, header_id: Optional[UUID]) -> UUID:
    tenant = resolve_tenant_id(user, header_id)
    if not tenant:
        raise ForbiddenError("Restaurant context required")
    return tenant


# Public menu by restaurant slug
@router.get("/public/{slug}/categories", response_model=List[CategoryOut])
def public_categories(slug: str, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.slug == slug).first()
    if not restaurant:
        raise NotFoundError("Restaurant not found")
    return MenuService(db).list_categories(restaurant.id)


@router.get("/public/{slug}/items", response_model=List[MenuItemOut])
def public_items(
    slug: str,
    category_id: Optional[UUID] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    restaurant = db.query(Restaurant).filter(Restaurant.slug == slug).first()
    if not restaurant:
        raise NotFoundError("Restaurant not found")
    return MenuService(db).list_items(
        restaurant.id, category_id=category_id, search=search, available_only=True
    )


@router.get("/menu/categories", response_model=List[CategoryOut])
def list_categories(
    db: Session = Depends(get_db),
    user: User = Depends(require_restaurant_access),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    return MenuService(db).list_categories(_tenant(user, header_id))


@router.post("/menu/categories", response_model=CategoryOut, status_code=201)
def create_category(
    payload: CategoryCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    if not user_has_permission(user, "menu:*") and not user_has_permission(user, "menu:edit"):
        raise ForbiddenError("Missing menu permission")
    return MenuService(db).create_category(_tenant(user, header_id), payload)


@router.patch("/menu/categories/{category_id}", response_model=CategoryOut)
def update_category(
    category_id: UUID,
    payload: CategoryUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    if not user_has_permission(user, "menu:*") and not user_has_permission(user, "menu:edit"):
        raise ForbiddenError("Missing menu permission")
    return MenuService(db).update_category(_tenant(user, header_id), category_id, payload)


@router.get("/menu/items", response_model=List[MenuItemOut])
def list_items(
    category_id: Optional[UUID] = None,
    search: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
    user: User = Depends(require_restaurant_access),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    return MenuService(db).list_items(
        _tenant(user, header_id), category_id=category_id, search=search
    )


@router.post("/menu/items", response_model=MenuItemOut, status_code=201)
def create_item(
    payload: MenuItemCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    if not user_has_permission(user, "menu:*") and not user_has_permission(user, "menu:edit"):
        raise ForbiddenError("Missing menu permission")
    return MenuService(db).create_item(_tenant(user, header_id), payload)


@router.get("/menu/items/{item_id}", response_model=MenuItemOut)
def get_item(
    item_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(require_restaurant_access),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    return MenuService(db).get_item(_tenant(user, header_id), item_id)


@router.patch("/menu/items/{item_id}", response_model=MenuItemOut)
def update_item(
    item_id: UUID,
    payload: MenuItemUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    if not user_has_permission(user, "menu:*") and not user_has_permission(user, "menu:edit"):
        raise ForbiddenError("Missing menu permission")
    return MenuService(db).update_item(_tenant(user, header_id), item_id, payload)


@router.delete("/menu/items/{item_id}", status_code=204)
def delete_item(
    item_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    if not user_has_permission(user, "menu:*"):
        raise ForbiddenError("Missing menu permission")
    MenuService(db).soft_delete_item(_tenant(user, header_id), item_id)
    return None
