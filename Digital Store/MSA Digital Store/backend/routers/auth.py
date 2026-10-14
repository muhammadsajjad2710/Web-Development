from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from models import User, Customer, UserRole
from schemas import CustomerRegister, LoginRequest, Token, UserOut, MessageOut
from auth import (
    get_password_hash,
    authenticate_user,
    build_token_response,
    get_current_user,
    require_roles,
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register_customer(payload: CustomerRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email.lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=payload.email.lower(),
        phone=payload.phone,
        full_name=payload.full_name,
        hashed_password=get_password_hash(payload.password),
        role=UserRole.customer,
    )
    db.add(user)
    db.flush()

    customer = Customer(
        user_id=user.id,
        address=payload.address,
        city=payload.city,
        district=payload.district,
    )
    db.add(customer)
    db.commit()
    db.refresh(user)
    return build_token_response(user, db)


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return build_token_response(user, db)


@router.post("/token", response_model=Token)
def login_form(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """OAuth2-compatible login for Swagger UI."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return build_token_response(user, db)


@router.post("/admin/login", response_model=Token)
def admin_login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.email, payload.password)
    if not user or user.role != UserRole.admin:
        raise HTTPException(status_code=401, detail="Invalid admin credentials")
    return build_token_response(user, db)


@router.post("/seller/login", response_model=Token)
def seller_login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.email, payload.password)
    if not user or user.role != UserRole.seller:
        raise HTTPException(status_code=401, detail="Invalid seller credentials")
    return build_token_response(user, db)


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user
