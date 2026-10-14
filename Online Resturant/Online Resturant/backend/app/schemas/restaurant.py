"""Restaurant and branch schemas."""

from datetime import time
from decimal import Decimal
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.schemas.common import TimestampSchema


class RestaurantCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    description: Optional[str] = None
    cuisine_type: Optional[str] = None
    contact_number: Optional[str] = None
    whatsapp_number: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: str = "Pakistan"
    delivery_available: bool = True
    pickup_available: bool = True
    dine_in_available: bool = True
    tax_rate: Decimal = Decimal("0.00")
    service_charge_rate: Decimal = Decimal("0.00")
    currency: str = "PKR"


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    cuisine_type: Optional[str] = None
    contact_number: Optional[str] = None
    whatsapp_number: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    logo_url: Optional[str] = None
    cover_image_url: Optional[str] = None
    opening_hours: Optional[Dict[str, Any]] = None
    delivery_available: Optional[bool] = None
    pickup_available: Optional[bool] = None
    dine_in_available: Optional[bool] = None
    tax_rate: Optional[Decimal] = None
    service_charge_rate: Optional[Decimal] = None
    currency: Optional[str] = None
    status: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None


class RestaurantOut(TimestampSchema):
    id: UUID
    name: str
    slug: str
    logo_url: Optional[str] = None
    cover_image_url: Optional[str] = None
    description: Optional[str] = None
    cuisine_type: Optional[str] = None
    contact_number: Optional[str] = None
    whatsapp_number: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: str
    delivery_available: bool
    pickup_available: bool
    dine_in_available: bool
    tax_rate: Decimal
    service_charge_rate: Decimal
    currency: str
    status: str
    opening_hours: Optional[Dict[str, Any]] = None


class BranchCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    address: Optional[str] = None
    contact_number: Optional[str] = None
    whatsapp_number: Optional[str] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None
    delivery_radius_km: Decimal = Decimal("5.00")
    manager_id: Optional[UUID] = None
    city: Optional[str] = None
    is_default: bool = False


class BranchUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    contact_number: Optional[str] = None
    whatsapp_number: Optional[str] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None
    delivery_radius_km: Optional[Decimal] = None
    manager_id: Optional[UUID] = None
    status: Optional[str] = None
    city: Optional[str] = None
    is_default: Optional[bool] = None


class BranchOut(TimestampSchema):
    id: UUID
    restaurant_id: UUID
    name: str
    address: Optional[str] = None
    contact_number: Optional[str] = None
    whatsapp_number: Optional[str] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None
    delivery_radius_km: Decimal
    manager_id: Optional[UUID] = None
    status: str
    city: Optional[str] = None
    is_default: bool
