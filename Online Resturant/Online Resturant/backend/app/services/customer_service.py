"""Customer / CRM service."""

from typing import List, Optional, Tuple
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.models.crm import CRMNote, Feedback
from app.models.customer import Customer
from app.schemas import CRMNoteCreate, CustomerCreate, CustomerUpdate, FeedbackCreate
from app.utils.helpers import paginate


class CustomerService:
    def __init__(self, db: Session):
        self.db = db

    def list(
        self,
        restaurant_id: UUID,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Tuple[List[Customer], dict]:
        query = self.db.query(Customer).filter(
            Customer.restaurant_id == restaurant_id, Customer.is_deleted.is_(False)
        )
        if search:
            like = f"%{search}%"
            query = query.filter(
                (Customer.full_name.ilike(like))
                | (Customer.phone.ilike(like))
                | (Customer.email.ilike(like))
            )
        total = query.count()
        items = (
            query.order_by(Customer.updated_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return items, paginate(total, page, page_size)

    def get(self, restaurant_id: UUID, customer_id: UUID) -> Customer:
        customer = (
            self.db.query(Customer)
            .filter(
                Customer.id == customer_id,
                Customer.restaurant_id == restaurant_id,
                Customer.is_deleted.is_(False),
            )
            .first()
        )
        if not customer:
            raise NotFoundError("Customer not found")
        return customer

    def create(self, restaurant_id: UUID, data: CustomerCreate) -> Customer:
        existing = (
            self.db.query(Customer)
            .filter(
                Customer.restaurant_id == restaurant_id,
                Customer.phone == data.phone,
                Customer.is_deleted.is_(False),
            )
            .first()
        )
        if existing:
            raise ConflictError("Customer with this phone already exists")
        customer = Customer(restaurant_id=restaurant_id, **data.model_dump())
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def update(self, restaurant_id: UUID, customer_id: UUID, data: CustomerUpdate) -> Customer:
        customer = self.get(restaurant_id, customer_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(customer, key, value)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def add_note(
        self, restaurant_id: UUID, data: CRMNoteCreate, created_by_id: Optional[UUID] = None
    ) -> CRMNote:
        self.get(restaurant_id, data.customer_id)
        note = CRMNote(
            restaurant_id=restaurant_id,
            created_by_id=created_by_id,
            **data.model_dump(),
        )
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def list_notes(self, restaurant_id: UUID, customer_id: Optional[UUID] = None) -> List[CRMNote]:
        query = self.db.query(CRMNote).filter(CRMNote.restaurant_id == restaurant_id)
        if customer_id:
            query = query.filter(CRMNote.customer_id == customer_id)
        return query.order_by(CRMNote.created_at.desc()).all()

    def add_feedback(self, restaurant_id: UUID, data: FeedbackCreate) -> Feedback:
        feedback = Feedback(restaurant_id=restaurant_id, **data.model_dump())
        self.db.add(feedback)
        self.db.commit()
        self.db.refresh(feedback)
        return feedback
