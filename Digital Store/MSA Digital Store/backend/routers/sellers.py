from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from database import get_db
from models import Seller, User, UserRole, SellerStatus, Product, Order, OrderItem
from schemas import (
    SellerRegister,
    SellerOut,
    SellerStatusUpdate,
    ProductOut,
    OrderOut,
    MessageOut,
)
from auth import get_password_hash, require_roles, get_current_user, get_seller_profile

router = APIRouter(prefix="/api/sellers", tags=["Sellers"])


@router.post("/register", response_model=SellerOut, status_code=201)
def register_seller(payload: SellerRegister, db: Session = Depends(get_db)):
    existing = db.query(Seller).filter(Seller.email == payload.email.lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Seller email already registered")

    user = None
    if payload.password:
        if db.query(User).filter(User.email == payload.email.lower()).first():
            raise HTTPException(status_code=400, detail="Email already has an account")
        user = User(
            email=payload.email.lower(),
            phone=payload.phone,
            full_name=payload.owner_name,
            hashed_password=get_password_hash(payload.password),
            role=UserRole.seller,
        )
        db.add(user)
        db.flush()

    seller = Seller(
        user_id=user.id if user else None,
        business_name=payload.business_name,
        owner_name=payload.owner_name,
        phone=payload.phone,
        email=payload.email.lower(),
        business_category=payload.business_category,
        business_address=payload.business_address,
        city=payload.city,
        district=payload.district,
        cnic=payload.cnic,
        ntn=payload.ntn,
        selling_type=payload.selling_type,
        status=SellerStatus.pending,
        is_verified=False,
    )
    db.add(seller)
    db.commit()
    db.refresh(seller)
    return seller


@router.get("", response_model=list[SellerOut])
def list_sellers(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin)),
):
    return db.query(Seller).order_by(Seller.created_at.desc()).all()


@router.get("/me", response_model=SellerOut)
def my_seller_profile(
    current_user: User = Depends(require_roles(UserRole.seller)),
    db: Session = Depends(get_db),
):
    return get_seller_profile(current_user, db)


@router.get("/{seller_id}", response_model=SellerOut)
def get_seller(seller_id: int, db: Session = Depends(get_db)):
    seller = db.query(Seller).filter(Seller.id == seller_id).first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    return seller


@router.put("/{seller_id}/status", response_model=SellerOut)
def update_seller_status(
    seller_id: int,
    payload: SellerStatusUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin)),
):
    seller = db.query(Seller).filter(Seller.id == seller_id).first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    seller.status = payload.status
    if payload.is_verified is not None:
        seller.is_verified = payload.is_verified
    elif payload.status == SellerStatus.approved:
        seller.is_verified = True
    db.commit()
    db.refresh(seller)
    return seller


@router.get("/{seller_id}/products", response_model=list[ProductOut])
def seller_products(seller_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Product)
        .options(joinedload(Product.category), joinedload(Product.seller), joinedload(Product.images))
        .filter(Product.seller_id == seller_id, Product.is_active == True)  # noqa: E712
        .all()
    )


@router.get("/{seller_id}/orders", response_model=list[OrderOut])
def seller_orders(
    seller_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == UserRole.seller:
        seller = get_seller_profile(current_user, db)
        if seller.id != seller_id:
            raise HTTPException(status_code=403, detail="Not allowed")
    elif current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not allowed")

    return (
        db.query(Order)
        .options(joinedload(Order.items))
        .join(OrderItem)
        .filter(OrderItem.seller_id == seller_id)
        .distinct()
        .order_by(Order.created_at.desc())
        .all()
    )


@router.get("/{seller_id}/payouts", response_model=MessageOut)
def seller_payouts_placeholder(seller_id: int):
    return {
        "message": "Seller payouts coming soon",
        "detail": "Placeholder for future payout gateway integration",
    }


@router.post("/{seller_id}/warehouse-request", response_model=MessageOut)
def warehouse_request_placeholder(seller_id: int):
    return {
        "message": "Warehouse request received",
        "detail": "MSA warehouse support request placeholder — automation coming soon",
    }
