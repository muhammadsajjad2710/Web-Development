"""Authentication service."""

from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from app.core.config import settings
from app.core.enums import PlanName, SubscriptionStatus, UserRole
from app.core.exceptions import ConflictError, NotFoundError, UnauthorizedError, ValidationAppError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.branch import Branch
from app.models.restaurant import Restaurant
from app.models.subscription import RestaurantSubscription, SubscriptionPlan
from app.models.user import Role, User
from app.schemas.auth import (
    LoginResponse,
    RestaurantRegisterRequest,
    UserOut,
    UserRegister,
)
from app.schemas.common import TokenPair
from app.utils.helpers import generate_reset_token, unique_slug


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def _get_role(self, role_name: str) -> Role:
        role = self.db.query(Role).filter(Role.name == role_name).first()
        if not role:
            raise NotFoundError(f"Role '{role_name}' is not configured. Run seed script.")
        return role

    def register_user(self, data: UserRegister, role_name: str = UserRole.CUSTOMER.value) -> User:
        existing = self.db.query(User).filter(User.email == data.email.lower()).first()
        if existing:
            raise ConflictError("Email already registered")

        role = self._get_role(role_name)
        user = User(
            email=data.email.lower(),
            phone=data.phone,
            password_hash=hash_password(data.password),
            full_name=data.full_name,
            role_id=role.id,
            is_active=True,
            is_verified=False,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return self._load_user(user.id)

    def register_restaurant(self, data: RestaurantRegisterRequest) -> LoginResponse:
        existing = self.db.query(User).filter(User.email == data.email.lower()).first()
        if existing:
            raise ConflictError("Email already registered")

        owner_role = self._get_role(UserRole.RESTAURANT_OWNER.value)
        slug = unique_slug(
            data.restaurant_name,
            lambda s: self.db.query(Restaurant).filter(Restaurant.slug == s).first() is not None,
        )

        restaurant = Restaurant(
            name=data.restaurant_name,
            slug=slug,
            cuisine_type=data.cuisine_type,
            city=data.city,
            country=data.country,
            contact_number=data.contact_number or data.phone,
            whatsapp_number=data.whatsapp_number or data.phone,
            address=data.address,
            email=data.email.lower(),
            currency="PKR",
            status="active",
            delivery_available=True,
            pickup_available=True,
            dine_in_available=True,
            opening_hours={
                "monday": {"open": "11:00", "close": "23:00"},
                "tuesday": {"open": "11:00", "close": "23:00"},
                "wednesday": {"open": "11:00", "close": "23:00"},
                "thursday": {"open": "11:00", "close": "23:00"},
                "friday": {"open": "11:00", "close": "23:30"},
                "saturday": {"open": "11:00", "close": "23:30"},
                "sunday": {"open": "12:00", "close": "23:00"},
            },
        )
        self.db.add(restaurant)
        self.db.flush()

        user = User(
            email=data.email.lower(),
            phone=data.phone,
            password_hash=hash_password(data.password),
            full_name=data.full_name,
            role_id=owner_role.id,
            restaurant_id=restaurant.id,
            is_active=True,
            is_verified=True,
        )
        self.db.add(user)
        self.db.flush()

        restaurant.owner_id = user.id

        branch = Branch(
            restaurant_id=restaurant.id,
            name=f"{data.restaurant_name} — Main",
            address=data.address,
            contact_number=data.contact_number or data.phone,
            whatsapp_number=data.whatsapp_number or data.phone,
            city=data.city,
            status="active",
            is_default=True,
            manager_id=user.id,
        )
        self.db.add(branch)

        plan = (
            self.db.query(SubscriptionPlan)
            .filter(SubscriptionPlan.name == PlanName.BASIC.value)
            .first()
        )
        if plan:
            now = datetime.now(timezone.utc)
            sub = RestaurantSubscription(
                restaurant_id=restaurant.id,
                plan_id=plan.id,
                status=SubscriptionStatus.TRIAL.value,
                trial_start=now,
                trial_end=now + timedelta(days=settings.DEFAULT_TRIAL_DAYS),
                billing_cycle="monthly",
            )
            self.db.add(sub)

        self.db.commit()
        user = self._load_user(user.id)
        return self._build_login_response(user)

    def login(self, email: str, password: str) -> LoginResponse:
        user = (
            self.db.query(User)
            .options(joinedload(User.role))
            .filter(User.email == email.lower(), User.is_deleted.is_(False))
            .first()
        )
        if not user or not verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid email or password")
        if not user.is_active:
            raise UnauthorizedError("Account is deactivated")

        user.last_login_at = datetime.now(timezone.utc)
        self.db.commit()
        user = self._load_user(user.id)
        return self._build_login_response(user)

    def refresh(self, refresh_token: str) -> TokenPair:
        try:
            payload = decode_token(refresh_token)
        except ValueError as exc:
            raise UnauthorizedError("Invalid refresh token") from exc
        if payload.get("type") != "refresh":
            raise UnauthorizedError("Invalid refresh token type")

        user = self._load_user(UUID(payload["sub"]))
        if not user or not user.is_active:
            raise UnauthorizedError("User not found or inactive")
        return self._issue_tokens(user)

    def forgot_password(self, email: str) -> str:
        user = self.db.query(User).filter(User.email == email.lower()).first()
        # Always return success message to avoid email enumeration
        if not user:
            return "If the email exists, a reset link has been sent."
        token = generate_reset_token()
        user.reset_token = token
        user.reset_token_expires = datetime.now(timezone.utc) + timedelta(hours=1)
        self.db.commit()
        # Email delivery is placeholder — token returned only in debug for testing
        return "If the email exists, a reset link has been sent."

    def reset_password(self, token: str, new_password: str) -> None:
        user = self.db.query(User).filter(User.reset_token == token).first()
        if not user or not user.reset_token_expires:
            raise ValidationAppError("Invalid or expired reset token")
        if user.reset_token_expires < datetime.now(timezone.utc):
            raise ValidationAppError("Reset token has expired")
        user.password_hash = hash_password(new_password)
        user.reset_token = None
        user.reset_token_expires = None
        self.db.commit()

    def _load_user(self, user_id: UUID) -> User:
        return (
            self.db.query(User)
            .options(joinedload(User.role))
            .filter(User.id == user_id)
            .first()
        )

    def _issue_tokens(self, user: User) -> TokenPair:
        claims = {
            "role": user.role.name if user.role else None,
            "restaurant_id": str(user.restaurant_id) if user.restaurant_id else None,
        }
        return TokenPair(
            access_token=create_access_token(user.id, claims),
            refresh_token=create_refresh_token(user.id, claims),
        )

    def _build_login_response(self, user: User) -> LoginResponse:
        return LoginResponse(tokens=self._issue_tokens(user), user=UserOut.model_validate(user))
