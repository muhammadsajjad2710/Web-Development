"""Restaurant and branch endpoints."""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.deps import (
    get_current_user,
    get_restaurant_id_header,
    require_restaurant_access,
    resolve_tenant_id,
    user_has_permission,
)
from app.core.exceptions import ForbiddenError
from app.db.session import get_db
from app.models.user import User
from app.schemas.restaurant import (
    BranchCreate,
    BranchOut,
    BranchUpdate,
    RestaurantOut,
    RestaurantUpdate,
)
from app.services.restaurant_service import BranchService, RestaurantService

router = APIRouter(tags=["restaurants"])


def _tenant(user: User, header_id: Optional[UUID]) -> UUID:
    tenant = resolve_tenant_id(user, header_id)
    if not tenant:
        raise ForbiddenError("Restaurant context required")
    return tenant


@router.get("/restaurants/public/{slug}", response_model=RestaurantOut)
def get_public_restaurant(slug: str, db: Session = Depends(get_db)):
    return RestaurantService(db).get_by_slug(slug)


@router.get("/restaurants/me", response_model=RestaurantOut)
def get_my_restaurant(
    db: Session = Depends(get_db),
    user: User = Depends(require_restaurant_access),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    return RestaurantService(db).get_by_id(_tenant(user, header_id))


@router.patch("/restaurants/me", response_model=RestaurantOut)
def update_my_restaurant(
    payload: RestaurantUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    if not user_has_permission(user, "settings:*") and not user_has_permission(
        user, "settings:branch"
    ):
        # Restaurant owners have settings:*
        if not user_has_permission(user, "dashboard:view"):
            raise ForbiddenError("Missing permission to update restaurant")
        # Only owner-level should fully update — check role
        from app.core.enums import UserRole

        if user.role.name not in (
            UserRole.SUPER_ADMIN.value,
            UserRole.RESTAURANT_OWNER.value,
        ):
            raise ForbiddenError("Only restaurant owners can update profile")
    return RestaurantService(db).update(_tenant(user, header_id), payload)


@router.get("/branches", response_model=List[BranchOut])
def list_branches(
    db: Session = Depends(get_db),
    user: User = Depends(require_restaurant_access),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    return BranchService(db).list(_tenant(user, header_id))


@router.post("/branches", response_model=BranchOut, status_code=201)
def create_branch(
    payload: BranchCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    if not (
        user_has_permission(user, "branches:*")
        or user.role.name in ("super_admin", "restaurant_owner")
    ):
        raise ForbiddenError("Missing branch management permission")
    return BranchService(db).create(_tenant(user, header_id), payload)


@router.get("/branches/{branch_id}", response_model=BranchOut)
def get_branch(
    branch_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(require_restaurant_access),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    return BranchService(db).get(_tenant(user, header_id), branch_id)


@router.patch("/branches/{branch_id}", response_model=BranchOut)
def update_branch(
    branch_id: UUID,
    payload: BranchUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    if not user_has_permission(user, "branches:*") and not user_has_permission(
        user, "settings:branch"
    ):
        raise ForbiddenError("Missing branch management permission")
    return BranchService(db).update(_tenant(user, header_id), branch_id, payload)


@router.delete("/branches/{branch_id}", status_code=204)
def delete_branch(
    branch_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    if not user_has_permission(user, "branches:*"):
        raise ForbiddenError("Missing branch management permission")
    BranchService(db).soft_delete(_tenant(user, header_id), branch_id)
    return None
