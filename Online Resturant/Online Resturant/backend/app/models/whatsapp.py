"""WhatsApp conversation, messages, and order session models."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.restaurant import Restaurant
    from app.models.customer import Customer
    from app.models.order import Order


class WhatsAppConversation(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "whatsapp_conversations"

    restaurant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    customer_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("customers.id", ondelete="SET NULL"), nullable=True
    )
    customer_phone: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    customer_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="active", nullable=False, index=True)
    human_handover: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    assigned_staff_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    last_message_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    meta: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    messages: Mapped[List["WhatsAppMessage"]] = relationship(
        "WhatsAppMessage", back_populates="conversation", cascade="all, delete-orphan"
    )
    sessions: Mapped[List["WhatsAppOrderSession"]] = relationship(
        "WhatsAppOrderSession", back_populates="conversation", cascade="all, delete-orphan"
    )


class WhatsAppMessage(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "whatsapp_messages"

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("whatsapp_conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    direction: Mapped[str] = mapped_column(String(16), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    message_type: Mapped[str] = mapped_column(String(32), default="text", nullable=False)
    intent: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    is_ai_generated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    external_message_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    meta: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    conversation: Mapped["WhatsAppConversation"] = relationship(
        "WhatsAppConversation", back_populates="messages"
    )


class WhatsAppOrderSession(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "whatsapp_order_sessions"

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("whatsapp_conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    restaurant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(String(32), default="started", nullable=False, index=True)
    cart: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    delivery_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    customer_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    order_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("orders.id", ondelete="SET NULL"), nullable=True
    )
    ai_context: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    conversation: Mapped["WhatsAppConversation"] = relationship(
        "WhatsAppConversation", back_populates="sessions"
    )
