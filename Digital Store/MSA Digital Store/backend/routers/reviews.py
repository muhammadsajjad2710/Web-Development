from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models import Review, Product, User, UserRole
from schemas import ReviewCreate, ReviewOut, MessageOut
from auth import require_roles, get_customer_profile

router = APIRouter(prefix="/api/reviews", tags=["Reviews"])


@router.get("/product/{product_id}", response_model=list[ReviewOut])
def product_reviews(product_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Review)
        .filter(Review.product_id == product_id)
        .order_by(Review.created_at.desc())
        .all()
    )


@router.post("", response_model=ReviewOut, status_code=201)
def add_review(
    payload: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.customer)),
):
    customer = get_customer_profile(current_user, db)
    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    review = Review(
        product_id=payload.product_id,
        customer_id=customer.id,
        rating=payload.rating,
        comment=payload.comment,
    )
    db.add(review)
    db.flush()

    avg = db.query(func.avg(Review.rating)).filter(Review.product_id == product.id).scalar() or 0
    count = db.query(func.count(Review.id)).filter(Review.product_id == product.id).scalar() or 0
    product.rating = round(float(avg), 1)
    product.review_count = count
    db.commit()
    db.refresh(review)
    return review
