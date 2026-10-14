from datetime import date, timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Installment, InstallmentPayment, User
from app.schemas import InstallmentPaymentCreate, InstallmentResponse

router = APIRouter(prefix="/api/installments", tags=["installments"])


@router.get("/", response_model=List[InstallmentResponse])
def list_installments(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    installments = db.query(Installment).order_by(Installment.id.desc()).all()
    return [
        InstallmentResponse(
            id=i.id,
            customer_name=i.customer.name if i.customer else "",
            product_name=i.product.name if i.product else "",
            total_amount=i.total_amount,
            down_payment=i.down_payment,
            remaining_balance=i.remaining_balance,
            monthly_amount=i.monthly_amount,
            total_months=i.total_months,
            next_due_date=i.next_due_date,
            status=i.status,
        )
        for i in installments
    ]


@router.post("/{installment_id}/pay")
def record_payment(
    installment_id: int,
    data: InstallmentPaymentCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    installment = db.query(Installment).filter(Installment.id == installment_id).first()
    if not installment:
        raise HTTPException(status_code=404, detail="Installment not found")
    if installment.status == "completed":
        raise HTTPException(status_code=400, detail="Installment already completed")

    if data.amount > installment.remaining_balance:
        raise HTTPException(status_code=400, detail="Payment exceeds remaining balance")

    payment = InstallmentPayment(
        installment_id=installment.id,
        amount=data.amount,
        payment_date=data.payment_date or date.today(),
        status="paid",
        notes=data.notes,
    )
    db.add(payment)

    installment.remaining_balance = round(installment.remaining_balance - data.amount, 2)
    if installment.remaining_balance <= 0:
        installment.remaining_balance = 0
        installment.status = "completed"
        installment.next_due_date = None
    else:
        installment.next_due_date = date.today() + timedelta(days=30)
        installment.status = "active"

    db.commit()
    return {"message": "Payment recorded", "remaining_balance": installment.remaining_balance}
