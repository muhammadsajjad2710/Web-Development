"""Authentication dependencies and RBAC helpers."""

from typing import Callable, List, Optional
from uuid import UUID

from fastapi import Depends, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session, joinedload

from app.core.enums import ROLE_PERMISSIONS, UserRole
from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.core.security import decode_token
from app.db.session import get_db
from app.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None or not credentials.credentials:
        raise UnauthorizedError("Authentication required")

    try:
        payload = decode_token(credentials.credentials)
    except ValueError as exc:
        raise UnauthorizedError("Invalid or expired token") from exc

    if payload.get("type") != "access":
        raise UnauthorizedError("Invalid token type")

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedError("Invalid token payload")

    user = (
        db.query(User)
        .options(joinedload(User.role))
        .filter(User.id == user_id, User.is_deleted.is_(False))
        .first()
    )
    if not user or not user.is_active:
        raise UnauthorizedError("User not found or inactive")
    return user


def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Optional[User]:
    if credentials is None:
        return None
    try:
        return get_current_user(credentials, db)
    except UnauthorizedError:
        return None


def get_restaurant_id_header(
    x_restaurant_id: Optional[str] = Header(default=None, alias="X-Restaurant-Id"),
) -> Optional[UUID]:
    if not x_restaurant_id:
        return None
    try:
        return UUID(x_restaurant_id)
    except ValueError as exc:
        raise ForbiddenError("Invalid restaurant id header") from exc


def resolve_tenant_id(
    user: User,
    header_restaurant_id: Optional[UUID] = None,
) -> Optional[UUID]:
    """Super admins may operate on any restaurant via header; others are locked to theirs."""
    role_name = user.role.name if user.role else None
    if role_name == UserRole.SUPER_ADMIN.value:
        return header_restaurant_id or user.restaurant_id
    return user.restaurant_id


def user_has_permission(user: User, permission: str) -> bool:
    role_name = user.role.name if user.role else None
    if not role_name:
        return False
    try:
        role = UserRole(role_name)
    except ValueError:
        return False

    allowed = ROLE_PERMISSIONS.get(role, [])
    if "*" in allowed:
        return True
    if permission in allowed:
        return True

    # Wildcard module match e.g. orders:* covers orders:view
    module = permission.split(":")[0]
    if f"{module}:*" in allowed:
        return True
    return False


def require_roles(*roles: UserRole) -> Callable:
    role_values = {r.value for r in roles}

    def dependency(user: User = Depends(get_current_user)) -> User:
        if not user.role or user.role.name not in role_values:
            raise ForbiddenError("Insufficient role privileges")
        return user

    return dependency


def require_permissions(*permissions: str) -> Callable:
    def dependency(user: User = Depends(get_current_user)) -> User:
        for perm in permissions:
            if not user_has_permission(user, perm):
                raise ForbiddenError(f"Missing permission: {perm}")
        return user

    return dependency


def require_restaurant_access(user: User = Depends(get_current_user)) -> User:
    role_name = user.role.name if user.role else None
    if role_name == UserRole.SUPER_ADMIN.value:
        return user
    if not user.restaurant_id:
        raise ForbiddenError("No restaurant associated with this account")
    return user
