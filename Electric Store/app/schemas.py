from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    full_name: str = "Admin"


class LoginRequest(BaseModel):
    username: str
    password: str


class ProductBase(BaseModel):
    name: str
    description: str = ""
    quantity: int = 0
    purchase_price: float
    sale_price: float
    low_stock_threshold: int = 3


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    purchase_price: Optional[float] = None
    sale_price: Optional[float] = None
    low_stock_threshold: Optional[int] = None


class ProductResponse(ProductBase):
    id: int
    image_path: str = ""
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CustomerBase(BaseModel):
    name: str
    phone: str
    cnic: str = ""
    address: str = ""


class CustomerCreate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SaleCreate(BaseModel):
    product_id: int
    customer_id: Optional[int] = None
    sale_type: Literal["cash", "installment"] = "cash"
    quantity: int = 1
    down_payment: float = 0
    total_months: int = 12
    notes: str = ""


class SaleResponse(BaseModel):
    id: int
    invoice_no: str
    product_id: int
    customer_id: Optional[int]
    sale_type: str
    quantity: int
    unit_price: float
    total_amount: float
    down_payment: float
    remaining_amount: float
    sale_date: datetime
    product_name: str = ""
    customer_name: str = ""

    class Config:
        from_attributes = True


class InstallmentPaymentCreate(BaseModel):
    amount: float
    payment_date: Optional[date] = None
    notes: str = ""


class InstallmentResponse(BaseModel):
    id: int
    customer_name: str
    product_name: str
    total_amount: float
    down_payment: float
    remaining_balance: float
    monthly_amount: float
    total_months: int
    next_due_date: Optional[date]
    status: str

    class Config:
        from_attributes = True


class ExpenseCreate(BaseModel):
    category: str
    description: str = ""
    amount: float
    expense_date: Optional[date] = None


class ExpenseResponse(BaseModel):
    id: int
    category: str
    description: str
    amount: float
    expense_date: date

    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    today_sales: float
    total_products: int
    low_stock_count: int
    remaining_installments: float
    monthly_profit: float
    monthly_expenses: float
    total_customers: int
    installments_due: int
