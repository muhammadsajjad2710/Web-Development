"""Branch model for multi-branch restaurants."""

from __future__ import annotations

import uuid
from datetime import time
from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, ForeignKey, Numeric, String, Text, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.restaurant import Restaurant
    from app.models.user import User
    from app.models.menu import BranchMenuItem
    from app.models.order import Order


class Branch(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "branches"

    restaurant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    contact_number: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    whatsapp_number: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    opening_time: Mapped[Optional[time]] = mapped_column(Time, nullable=True)
    closing_time: Mapped[Optional[time]] = mapped_column(Time, nullable=True)
    delivery_radius_km: Mapped[Decimal] = mapped_column(
        Numeric(6, 2), default=Decimal("5.00"), nullable=False
    )
    manager_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[str] = mapped_column(String(32), default="active", nullable=False, index=True)
    city: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    latitude: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 7), nullable=True)
    longitude: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 7), nullable=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    restaurant: Mapped["Restaurant"] = relationship("Restaurant", back_populates="branches")
    manager: Mapped[Optional["User"]] = relationship("User", foreign_keys=[manager_id])
    menu_availability: Mapped[List["BranchMenuItem"]] = relationship(
        "BranchMenuItem", back_populates="branch", cascade="all, delete-orphan"
    )
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="branch")
