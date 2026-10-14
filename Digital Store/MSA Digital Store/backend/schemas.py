from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from models import (
    UserRole,
    ProductBadge,
    StockStatus,
    OrderStatus,
    PaymentMethod,
    PaymentStatus,
    SellingType,
    SellerStatus,
)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: UserRole
    user_id: int
    full_name: str
    customer_id: Optional[int] = None
    seller_id: Optional[int] = None


class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[UserRole] = None


class CustomerRegister(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    email: EmailStr
    phone: Optional[str] = None
    password: str = Field(min_length=6)
    address: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    full_name: str
    phone: Optional[str] = None
    role: UserRole
    is_active: bool
    created_at: datetime


class CategoryCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    icon: Optional[str] = None


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None


class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    description: Optional[str] = None
    icon: Optional[str] = None


class ProductImageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    is_primary: bool
    alt_text: Optional[str] = None


class SellerBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    business_name: str
    is_verified: bool
    status: SellerStatus


class ProductCreate(BaseModel):
    name: str
    slug: Optional[str] = None
    description: str
    features: Optional[str] = None
    price: float
    original_price: Optional[float] = None
    badge: ProductBadge = ProductBadge.verified_seller
    stock: int = 0
    warehouse_available: bool = False
    category_id: int
    seller_id: int
    image_url: Optional[str] = None
    delivery_info: Optional[str] = None
    return_policy: Optional[str] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    features: Optional[str] = None
    price: Optional[float] = None
    original_price: Optional[float] = None
    badge: Optional[ProductBadge] = None
    stock: Optional[int] = None
    warehouse_available: Optional[bool] = None
    category_id: Optional[int] = None
    seller_id: Optional[int] = None
    image_url: Optional[str] = None
    delivery_info: Optional[str] = None
    return_policy: Optional[str] = None
    is_active: Optional[bool] = None


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    description: str
    features: Optional[str] = None
    price: float
    original_price: Optional[float] = None
    badge: ProductBadge
    stock: int
    stock_status: StockStatus
    warehouse_available: bool
    rating: float
    review_count: int
    delivery_info: Optional[str] = None
    return_policy: Optional[str] = None
    is_active: bool
    category_id: int
    seller_id: int
    category: Optional[CategoryOut] = None
    seller: Optional[SellerBrief] = None
    images: list[ProductImageOut] = []
    created_at: datetime


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(default=1, ge=1)


class CartItemUpdate(BaseModel):
    quantity: int = Field(ge=1)


class CartItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    product: Optional[ProductOut] = None


class CartOut(BaseModel):
    items: list[CartItemOut]
    subtotal: float
    delivery_charges: float
    total: float
    item_count: int


class OrderCreate(BaseModel):
    customer_name: str
    phone: str
    email: Optional[EmailStr] = None
    address: str
    city: str
    district: str
    payment_method: PaymentMethod
    notes: Optional[str] = None
    # Guest checkout: items from localStorage when not logged in
    guest_items: Optional[list[CartItemCreate]] = None


class OrderItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    product_name: str
    unit_price: float
    quantity: int
    line_total: float
    seller_id: Optional[int] = None


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_number: str
    customer_id: int
    customer_name: str
    phone: str
    email: Optional[str] = None
    address: str
    city: str
    district: str
    payment_method: PaymentMethod
    status: OrderStatus
    subtotal: float
    delivery_charges: float
    total_amount: float
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemOut] = []


class SellerRegister(BaseModel):
    business_name: str
    owner_name: str
    phone: str
    email: EmailStr
    business_category: str
    business_address: str
    city: str
    district: str
    cnic: Optional[str] = None
    ntn: Optional[str] = None
    selling_type: SellingType = SellingType.own_shop
    password: Optional[str] = Field(default=None, min_length=6)


class SellerOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    business_name: str
    owner_name: str
    phone: str
    email: str
    business_category: str
    business_address: str
    city: str
    district: str
    cnic: Optional[str] = None
    ntn: Optional[str] = None
    selling_type: SellingType
    status: SellerStatus
    is_verified: bool
    created_at: datetime


class SellerStatusUpdate(BaseModel):
    status: SellerStatus
    is_verified: Optional[bool] = None


class InventoryUpdate(BaseModel):
    quantity: int = Field(ge=0)
    low_stock_threshold: Optional[int] = Field(default=None, ge=1)
    warehouse_location: Optional[str] = None


class InventoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    low_stock_threshold: int
    warehouse_location: Optional[str] = None
    updated_at: datetime
    product: Optional[ProductOut] = None


class ReviewCreate(BaseModel):
    product_id: int
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None


class ReviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    customer_id: int
    rating: int
    comment: Optional[str] = None
    created_at: datetime


class WishlistCreate(BaseModel):
    product_id: int


class WishlistOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    product: Optional[ProductOut] = None
    created_at: datetime


class DashboardStats(BaseModel):
    total_orders: int
    total_sales: float
    total_products: int
    total_customers: int
    active_sellers: int
    low_stock_products: int
    pending_orders: int
    returned_orders: int
    recent_orders: list[OrderOut] = []
    top_selling_products: list[dict] = []


class MessageOut(BaseModel):
    message: str
    detail: Optional[str] = None
