from datetime import datetime, date

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), default="Admin")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, default="")
    quantity = Column(Integer, default=0)
    purchase_price = Column(Float, nullable=False)
    sale_price = Column(Float, nullable=False)
    image_path = Column(String(255), default="")
    low_stock_threshold = Column(Integer, default=3)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sales = relationship("Sale", back_populates="product")


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    phone = Column(String(20), nullable=False)
    cnic = Column(String(20), default="")
    address = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    sales = relationship("Sale", back_populates="customer")
    installments = relationship("Installment", back_populates="customer")


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    invoice_no = Column(String(30), unique=True, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    sale_type = Column(String(20), nullable=False)  # cash | installment
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    down_payment = Column(Float, default=0)
    remaining_amount = Column(Float, default=0)
    sale_date = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text, default="")

    product = relationship("Product", back_populates="sales")
    customer = relationship("Customer", back_populates="sales")
    installment = relationship("Installment", back_populates="sale", uselist=False)


class Installment(Base):
    __tablename__ = "installments"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"), unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    down_payment = Column(Float, default=0)
    remaining_balance = Column(Float, nullable=False)
    monthly_amount = Column(Float, nullable=False)
    total_months = Column(Integer, nullable=False)
    start_date = Column(Date, default=date.today)
    next_due_date = Column(Date, nullable=True)
    status = Column(String(20), default="active")  # active | completed | overdue
    created_at = Column(DateTime, default=datetime.utcnow)

    sale = relationship("Sale", back_populates="installment")
    customer = relationship("Customer", back_populates="installments")
    product = relationship("Product")
    payments = relationship("InstallmentPayment", back_populates="installment")


class InstallmentPayment(Base):
    __tablename__ = "installment_payments"

    id = Column(Integer, primary_key=True, index=True)
    installment_id = Column(Integer, ForeignKey("installments.id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(Date, default=date.today)
    due_date = Column(Date, nullable=True)
    status = Column(String(20), default="paid")  # paid | pending | overdue
    notes = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    installment = relationship("Installment", back_populates="payments")


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), nullable=False)
    description = Column(String(255), default="")
    amount = Column(Float, nullable=False)
    expense_date = Column(Date, default=date.today)
    created_at = Column(DateTime, default=datetime.utcnow)
