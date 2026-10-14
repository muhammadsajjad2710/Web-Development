"""Order schemas."""

from decimal import Decimal
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import TimestampSchema


class OrderItemIn(BaseModel):
    menu_item_id: UUID
    quantity: int = Field(ge=1, le=99)
    variation: Optional[Dict[str, Any]] = None
    addons: Optional[List[Dict[str, Any]]] = None
    notes: Optional[str] = None


class OrderCreate(BaseModel):
    branch_id: Optional[UUID] = None
    order_type: str = "delivery"
    customer_name: str = Field(min_length=2, max_length=255)
    customer_phone: str = Field(min_length=7, max_length=32)
    customer_email: Optional[str] = None
    delivery_address: Optional[str] = None
    special_instructions: Optional[str] = None
    payment_method: str = "cod"
    items: List[OrderItemIn] = Field(min_length=1)


class OrderStatusUpdate(BaseModel):
    status: str
    note: Optional[str] = None


class AssignRiderRequest(BaseModel):
    rider_id: UUID


class OrderItemOut(TimestampSchema):
    id: UUID
    menu_item_id: Optional[UUID] = None
    item_name: str
    quantity: int
    unit_price: Decimal
    total_price: Decimal
    variation: Optional[Dict[str, Any]] = None
    addons: Optional[List[Any]] = None
    notes: Optional[str] = None


class OrderOut(TimestampSchema):
    id: UUID
    restaurant_id: UUID
    branch_id: Optional[UUID] = None
    customer_id: Optional[UUID] = None
    order_number: str
    order_type: str
    status: str
    payment_status: str
    payment_method: str
    customer_name: str
    customer_phone: str
    customer_email: Optional[str] = None
    delivery_address: Optional[str] = None
    special_instructions: Optional[str] = None
    subtotal: Decimal
    tax_amount: Decimal
    service_charge: Decimal
    delivery_fee: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    currency: str
    source: str
    assigned_rider_id: Optional[UUID] = None
    items: List[OrderItemOut] = []


class OrderListItem(TimestampSchema):
    id: UUID
    order_number: str
    status: str
    order_type: str
    customer_name: str
    customer_phone: str
    total_amount: Decimal
    currency: str
    payment_status: str
    source: str
