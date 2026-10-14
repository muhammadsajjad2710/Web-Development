"""Menu schemas."""

from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import TimestampSchema


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    description: Optional[str] = None
    parent_id: Optional[UUID] = None
    image_url: Optional[str] = None
    sort_order: int = 0


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[UUID] = None
    image_url: Optional[str] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None


class CategoryOut(TimestampSchema):
    id: UUID
    restaurant_id: UUID
    parent_id: Optional[UUID] = None
    name: str
    slug: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    sort_order: int
    is_active: bool


class VariationIn(BaseModel):
    name: str
    price_delta: Decimal = Decimal("0.00")
    is_default: bool = False


class AddonIn(BaseModel):
    name: str
    price: Decimal = Decimal("0.00")
    max_quantity: int = 5


class MenuItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    category_id: Optional[UUID] = None
    description: Optional[str] = None
    price: Decimal
    discount_price: Optional[Decimal] = None
    image_url: Optional[str] = None
    preparation_time_minutes: int = 20
    is_popular: bool = False
    is_featured: bool = False
    spice_level: str = "none"
    serving_size: Optional[str] = None
    variations: List[VariationIn] = []
    addons: List[AddonIn] = []


class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[UUID] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    discount_price: Optional[Decimal] = None
    image_url: Optional[str] = None
    preparation_time_minutes: Optional[int] = None
    is_available: Optional[bool] = None
    is_popular: Optional[bool] = None
    is_featured: Optional[bool] = None
    spice_level: Optional[str] = None
    serving_size: Optional[str] = None
    sort_order: Optional[int] = None


class VariationOut(TimestampSchema):
    id: UUID
    name: str
    price_delta: Decimal
    is_default: bool
    is_available: bool


class AddonOut(TimestampSchema):
    id: UUID
    name: str
    price: Decimal
    is_available: bool
    max_quantity: int


class MenuItemOut(TimestampSchema):
    id: UUID
    restaurant_id: UUID
    category_id: Optional[UUID] = None
    name: str
    slug: str
    description: Optional[str] = None
    price: Decimal
    discount_price: Optional[Decimal] = None
    image_url: Optional[str] = None
    preparation_time_minutes: int
    is_available: bool
    is_popular: bool
    is_featured: bool
    spice_level: str
    serving_size: Optional[str] = None
    variations: List[VariationOut] = []
    addons: List[AddonOut] = []
