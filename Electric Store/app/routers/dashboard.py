from datetime import date, datetime

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Expense, Installment, Product, Sale, User
from app.schemas import DashboardStats

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    today_start = datetime.combine(date.today(), datetime.min.time())

    today_sales = (
        db.query(func.coalesce(func.sum(Sale.total_amount), 0))
        .filter(Sale.sale_date >= today_start)
        .scalar()
    )

    total_products = db.query(func.count(Product.id)).scalar() or 0

    low_stock_count = (
        db.query(func.count(Product.id))
        .filter(Product.quantity <= Product.low_stock_threshold)
        .scalar()
        or 0
    )

    remaining_installments = (
        db.query(func.coalesce(func.sum(Installment.remaining_balance), 0))
        .filter(Installment.status.in_(["active", "overdue"]))
        .scalar()
    )

    month_start = date.today().replace(day=1)
    month_start_dt = datetime.combine(month_start, datetime.min.time())

    monthly_sales = (
        db.query(func.coalesce(func.sum(Sale.total_amount), 0))
        .filter(Sale.sale_date >= month_start_dt)
        .scalar()
    )

    monthly_purchase_cost = (
        db.query(func.coalesce(func.sum(Sale.quantity * Product.purchase_price), 0))
        .join(Product, Sale.product_id == Product.id)
        .filter(Sale.sale_date >= month_start_dt)
        .scalar()
    )

    monthly_expenses = (
        db.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(Expense.expense_date >= month_start)
        .scalar()
    )

    monthly_profit = float(monthly_sales) - float(monthly_purchase_cost) - float(monthly_expenses)

    installments_due = (
        db.query(func.count(Installment.id))
        .filter(
            Installment.status.in_(["active", "overdue"]),
            Installment.next_due_date <= date.today(),
        )
        .scalar()
        or 0
    )

    from app.models import Customer

    total_customers = db.query(func.count(Customer.id)).scalar() or 0

    return DashboardStats(
        today_sales=float(today_sales),
        total_products=total_products,
        low_stock_count=low_stock_count,
        remaining_installments=float(remaining_installments),
        monthly_profit=monthly_profit,
        monthly_expenses=float(monthly_expenses),
        total_customers=total_customers,
        installments_due=installments_due,
    )


@router.get("/charts")
def get_chart_data(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    # Last 6 months sales
    sales_by_month = []
    for i in range(5, -1, -1):
        month_date = date.today().replace(day=1)
        if month_date.month - i <= 0:
            m = 12 + (month_date.month - i)
            y = month_date.year - 1
        else:
            m = month_date.month - i
            y = month_date.year
        start = date(y, m, 1)
        if m == 12:
            end = date(y + 1, 1, 1)
        else:
            end = date(y, m + 1, 1)
        total = (
            db.query(func.coalesce(func.sum(Sale.total_amount), 0))
            .filter(Sale.sale_date >= datetime.combine(start, datetime.min.time()))
            .filter(Sale.sale_date < datetime.combine(end, datetime.min.time()))
            .scalar()
        )
        sales_by_month.append({"month": start.strftime("%b"), "amount": float(total)})

    # Product stock levels
    products = db.query(Product).all()
    stock_data = [{"name": p.name[:20], "quantity": p.quantity} for p in products]

    # Expense breakdown
    expenses = (
        db.query(Expense.category, func.sum(Expense.amount))
        .group_by(Expense.category)
        .all()
    )
    expense_data = [{"category": cat, "amount": float(amt)} for cat, amt in expenses]

    return {
        "sales_by_month": sales_by_month,
        "stock_data": stock_data,
        "expense_data": expense_data,
    }
