"""Restaurant tenant model."""

from __future__ import annotations

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, Numeric, String, Text, Time
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.branch import Branch
    from app.models.user import User
    from app.models.subscription import RestaurantSubscription
    from app.models.menu import Category, MenuItem
    from app.models.order import Order
    from app.models.customer import Customer


class Restaurant(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "restaurants"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    logo_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    cover_image_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    cuisine_type: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    contact_number: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    whatsapp_number: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(128), nullable=True, index=True)
    country: Mapped[str] = mapped_column(String(128), default="Pakistan", nullable=False)
    latitude: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 7), nullable=True)
    longitude: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 7), nullable=True)
    opening_hours: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    delivery_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    pickup_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    dine_in_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    tax_rate: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("0.00"), nullable=False)
    service_charge_rate: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), default=Decimal("0.00"), nullable=False
    )
    currency: Mapped[str] = mapped_column(String(8), default="PKR", nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="pending", nullable=False, index=True)
    settings: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    owner_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)

    users: Mapped[List["User"]] = relationship(
        "User", back_populates="restaurant", foreign_keys="User.restaurant_id"
    )
    branches: Mapped[List["Branch"]] = relationship(
        "Branch", back_populates="restaurant", cascade="all, delete-orphan"
    )
    categories: Mapped[List["Category"]] = relationship(
        "Category", back_populates="restaurant", cascade="all, delete-orphan"
    )
    menu_items: Mapped[List["MenuItem"]] = relationship(
        "MenuItem", back_populates="restaurant", cascade="all, delete-orphan"
    )
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="restaurant")
    customers: Mapped[List["Customer"]] = relationship("Customer", back_populates="restaurant")
    subscription: Mapped[Optional["RestaurantSubscription"]] = relationship(
        "RestaurantSubscription", back_populates="restaurant", uselist=False
    )
