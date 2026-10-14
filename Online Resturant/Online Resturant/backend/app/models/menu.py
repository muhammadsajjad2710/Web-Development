"""Digital menu models: categories, items, variations, addons, deals, combos."""

from __future__ import annotations

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.restaurant import Restaurant
    from app.models.branch import Branch


class Category(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "categories"

    restaurant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    slug: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    restaurant: Mapped["Restaurant"] = relationship("Restaurant", back_populates="categories")
    parent: Mapped[Optional["Category"]] = relationship(
        "Category", remote_side="Category.id", backref="subcategories"
    )
    items: Mapped[List["MenuItem"]] = relationship("MenuItem", back_populates="category")


class MenuItem(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "menu_items"

    restaurant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    category_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    discount_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    preparation_time_minutes: Mapped[int] = mapped_column(Integer, default=20, nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    is_popular: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    spice_level: Mapped[str] = mapped_column(String(32), default="none", nullable=False)
    serving_size: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    calories: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    tags: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)

    restaurant: Mapped["Restaurant"] = relationship("Restaurant", back_populates="menu_items")
    category: Mapped[Optional["Category"]] = relationship("Category", back_populates="items")
    variations: Mapped[List["ItemVariation"]] = relationship(
        "ItemVariation", back_populates="menu_item", cascade="all, delete-orphan"
    )
    addons: Mapped[List["ItemAddon"]] = relationship(
        "ItemAddon", back_populates="menu_item", cascade="all, delete-orphan"
    )
    branch_availability: Mapped[List["BranchMenuItem"]] = relationship(
        "BranchMenuItem", back_populates="menu_item", cascade="all, delete-orphan"
    )


class ItemVariation(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "item_variations"

    menu_item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("menu_items.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    price_delta: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0.00"), nullable=False)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    menu_item: Mapped["MenuItem"] = relationship("MenuItem", back_populates="variations")


class ItemAddon(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "item_addons"

    menu_item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("menu_items.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0.00"), nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    max_quantity: Mapped[int] = mapped_column(Integer, default=5, nullable=False)

    menu_item: Mapped["MenuItem"] = relationship("MenuItem", back_populates="addons")


class Deal(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "deals"

    restaurant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    original_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    items_config: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    valid_from: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    valid_until: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class Combo(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "combos"

    restaurant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    image_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    items_config: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class BranchMenuItem(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "branch_menu_items"
    __table_args__ = (
        UniqueConstraint("branch_id", "menu_item_id", name="uq_branch_menu_item"),
    )

    branch_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("branches.id", ondelete="CASCADE"), nullable=False, index=True
    )
    menu_item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("menu_items.id", ondelete="CASCADE"), nullable=False, index=True
    )
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    price_override: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True)

    branch: Mapped["Branch"] = relationship("Branch", back_populates="menu_availability")
    menu_item: Mapped["MenuItem"] = relationship("MenuItem", back_populates="branch_availability")
