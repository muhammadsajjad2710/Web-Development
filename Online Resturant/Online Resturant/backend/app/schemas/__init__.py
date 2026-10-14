"""Customer, CRM, dashboard, WhatsApp, AI, and subscription schemas."""

from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import TimestampSchema


# --- Customers / CRM ---

class CustomerCreate(BaseModel):
    full_name: str
    phone: str
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    notes: Optional[str] = None


class CustomerUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None


class CustomerOut(TimestampSchema):
    id: UUID
    restaurant_id: UUID
    full_name: str
    phone: str
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    total_orders: int
    total_spent: Decimal
    loyalty_points: int
    favorite_items: Optional[List[Any]] = None
    last_order_at: Optional[datetime] = None
    notes: Optional[str] = None


class CRMNoteCreate(BaseModel):
    customer_id: UUID
    note_type: str = "general"
    title: Optional[str] = None
    body: str
    is_complaint: bool = False


class CRMNoteOut(TimestampSchema):
    id: UUID
    restaurant_id: UUID
    customer_id: UUID
    created_by_id: Optional[UUID] = None
    note_type: str
    title: Optional[str] = None
    body: str
    is_complaint: bool


class FeedbackCreate(BaseModel):
    customer_id: Optional[UUID] = None
    order_id: Optional[UUID] = None
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None
    is_public: bool = True


# --- Dashboard ---

class DashboardStats(BaseModel):
    total_orders: int
    today_orders: int
    pending_orders: int
    completed_orders: int
    cancelled_orders: int
    total_revenue: Decimal
    today_revenue: Decimal
    customer_count: int
    repeat_customers: int
    top_selling_items: List[Dict[str, Any]]
    recent_orders: List[Dict[str, Any]]
    sales_by_day: List[Dict[str, Any]]
    orders_by_status: List[Dict[str, Any]]


# --- WhatsApp ---

class WhatsAppInboundMessage(BaseModel):
    restaurant_id: UUID
    customer_phone: str
    customer_name: Optional[str] = None
    body: str
    external_message_id: Optional[str] = None


class WhatsAppMessageOut(TimestampSchema):
    id: UUID
    conversation_id: UUID
    direction: str
    body: str
    message_type: str
    intent: Optional[str] = None
    is_ai_generated: bool


class WhatsAppConversationOut(TimestampSchema):
    id: UUID
    restaurant_id: UUID
    customer_phone: str
    customer_name: Optional[str] = None
    status: str
    human_handover: bool
    last_message_at: Optional[datetime] = None


class HumanHandoverRequest(BaseModel):
    enabled: bool = True
    staff_id: Optional[UUID] = None


# --- AI placeholders ---

class AIChatRequest(BaseModel):
    restaurant_id: UUID
    message: str
    language: str = "en"
    session_id: Optional[str] = None


class AIChatResponse(BaseModel):
    reply: str
    intent: Optional[str] = None
    language: str
    requires_human: bool = False
    meta: Optional[Dict[str, Any]] = None


class AICallLogCreate(BaseModel):
    restaurant_id: UUID
    caller_number: str
    called_number: Optional[str] = None
    status: str = "ringing"
    provider: str = "twilio"
    external_call_id: Optional[str] = None


class AICallLogOut(TimestampSchema):
    id: UUID
    restaurant_id: UUID
    caller_number: str
    status: str
    transcript: Optional[str] = None
    summary: Optional[str] = None
    language: str
    human_followup_required: bool
    order_id: Optional[UUID] = None


# --- Subscriptions ---

class SubscriptionPlanOut(TimestampSchema):
    id: UUID
    name: str
    display_name: str
    description: Optional[str] = None
    price_monthly: Decimal
    price_yearly: Optional[Decimal] = None
    currency: str
    max_branches: int
    max_staff: int
    max_menu_items: int
    features: Dict[str, Any]
    is_active: bool


class RestaurantSubscriptionOut(TimestampSchema):
    id: UUID
    restaurant_id: UUID
    plan: SubscriptionPlanOut
    status: str
    trial_start: Optional[datetime] = None
    trial_end: Optional[datetime] = None
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    billing_cycle: str
