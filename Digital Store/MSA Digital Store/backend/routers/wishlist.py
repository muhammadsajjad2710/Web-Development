from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from database import get_db
from models import WishlistItem, Product, User, UserRole
from schemas import WishlistCreate, WishlistOut, MessageOut
from auth import require_roles, get_customer_profile

router = APIRouter(prefix="/api/wishlist", tags=["Wishlist"])


@router.get("", response_model=list[WishlistOut])
def get_wishlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.customer)),
):
    customer = get_customer_profile(current_user, db)
    return (
        db.query(WishlistItem)
        .options(
            joinedload(WishlistItem.product).joinedload(Product.images),
            joinedload(WishlistItem.product).joinedload(Product.category),
            joinedload(WishlistItem.product).joinedload(Product.seller),
        )
        .filter(WishlistItem.customer_id == customer.id)
        .all()
    )


@router.post("", response_model=WishlistOut, status_code=201)
def add_wishlist(
    payload: WishlistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.customer)),
):
    customer = get_customer_profile(current_user, db)
    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    existing = (
        db.query(WishlistItem)
        .filter(WishlistItem.customer_id == customer.id, WishlistItem.product_id == payload.product_id)
        .first()
    )
    if existing:
        return existing

    item = WishlistItem(customer_id=customer.id, product_id=payload.product_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return (
        db.query(WishlistItem)
        .options(joinedload(WishlistItem.product).joinedload(Product.images))
        .filter(WishlistItem.id == item.id)
        .first()
    )


@router.delete("/{product_id}", response_model=MessageOut)
def remove_wishlist(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.customer)),
):
    customer = get_customer_profile(current_user, db)
    item = (
        db.query(WishlistItem)
        .filter(WishlistItem.customer_id == customer.id, WishlistItem.product_id == product_id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Wishlist item not found")
    db.delete(item)
    db.commit()
    return {"message": "Removed from wishlist"}
