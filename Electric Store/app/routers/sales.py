from datetime import date, timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Customer, Installment, Product, Sale, User
from app.schemas import SaleCreate, SaleResponse

router = APIRouter(prefix="/api/sales", tags=["sales"])


def _next_invoice_no(db: Session) -> str:
    last = db.query(Sale).order_by(Sale.id.desc()).first()
    num = (last.id + 1) if last else 1001
    return f"INV-{num}"


@router.get("/", response_model=List[SaleResponse])
def list_sales(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    sales = db.query(Sale).order_by(Sale.id.desc()).all()
    result = []
    for s in sales:
        result.append(
            SaleResponse(
                id=s.id,
                invoice_no=s.invoice_no,
                product_id=s.product_id,
                customer_id=s.customer_id,
                sale_type=s.sale_type,
                quantity=s.quantity,
                unit_price=s.unit_price,
                total_amount=s.total_amount,
                down_payment=s.down_payment,
                remaining_amount=s.remaining_amount,
                sale_date=s.sale_date,
                product_name=s.product.name if s.product else "",
                customer_name=s.customer.name if s.customer else "Walk-in",
            )
        )
    return result


@router.post("/", response_model=SaleResponse)
def create_sale(
    data: SaleCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.quantity < data.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    if data.sale_type == "installment" and not data.customer_id:
        raise HTTPException(status_code=400, detail="Customer required for installment sale")

    total = product.sale_price * data.quantity
    remaining = 0.0
    down = data.down_payment

    if data.sale_type == "installment":
        if down >= total:
            raise HTTPException(status_code=400, detail="Down payment must be less than total")
        remaining = total - down
        if data.total_months <= 0:
            raise HTTPException(status_code=400, detail="Invalid installment months")

    sale = Sale(
        invoice_no=_next_invoice_no(db),
        product_id=product.id,
        customer_id=data.customer_id,
        sale_type=data.sale_type,
        quantity=data.quantity,
        unit_price=product.sale_price,
        total_amount=total,
        down_payment=down if data.sale_type == "installment" else total,
        remaining_amount=remaining,
        notes=data.notes,
    )
    product.quantity -= data.quantity
    db.add(sale)
    db.flush()

    if data.sale_type == "installment":
        monthly = round(remaining / data.total_months, 2)
        installment = Installment(
            sale_id=sale.id,
            customer_id=data.customer_id,
            product_id=product.id,
            total_amount=total,
            down_payment=down,
            remaining_balance=remaining,
            monthly_amount=monthly,
            total_months=data.total_months,
            start_date=date.today(),
            next_due_date=date.today() + timedelta(days=30),
            status="active",
        )
        db.add(installment)

    db.commit()
    db.refresh(sale)

    customer_name = "Walk-in"
    if sale.customer_id:
        c = db.query(Customer).filter(Customer.id == sale.customer_id).first()
        customer_name = c.name if c else "Walk-in"

    return SaleResponse(
        id=sale.id,
        invoice_no=sale.invoice_no,
        product_id=sale.product_id,
        customer_id=sale.customer_id,
        sale_type=sale.sale_type,
        quantity=sale.quantity,
        unit_price=sale.unit_price,
        total_amount=sale.total_amount,
        down_payment=sale.down_payment,
        remaining_amount=sale.remaining_amount,
        sale_date=sale.sale_date,
        product_name=product.name,
        customer_name=customer_name,
    )
