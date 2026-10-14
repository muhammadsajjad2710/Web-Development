from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Expense, User
from app.schemas import ExpenseCreate, ExpenseResponse

router = APIRouter(prefix="/api/expenses", tags=["expenses"])


@router.get("/", response_model=List[ExpenseResponse])
def list_expenses(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return db.query(Expense).order_by(Expense.expense_date.desc()).all()


@router.post("/", response_model=ExpenseResponse)
def create_expense(
    data: ExpenseCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    expense = Expense(
        category=data.category,
        description=data.description,
        amount=data.amount,
        expense_date=data.expense_date,
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense
