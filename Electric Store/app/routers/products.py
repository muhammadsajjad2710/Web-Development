import os
import uuid
from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.config import UPLOAD_DIR
from app.database import get_db
from app.models import Product, User
from app.schemas import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/api/products", tags=["products"])

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def _save_image(file: UploadFile) -> str:
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid image format")
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(file.file.read())
    return f"/static/uploads/{filename}"


@router.get("/", response_model=List[ProductResponse])
def list_products(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return db.query(Product).order_by(Product.id.desc()).all()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductResponse)
async def create_product(
    name: str = Form(...),
    description: str = Form(""),
    quantity: int = Form(0),
    purchase_price: float = Form(...),
    sale_price: float = Form(...),
    low_stock_threshold: int = Form(3),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    image_path = ""
    if image and image.filename:
        image_path = _save_image(image)

    product = Product(
        name=name,
        description=description,
        quantity=quantity,
        purchase_price=purchase_price,
        sale_price=sale_price,
        low_stock_threshold=low_stock_threshold,
        image_path=image_path,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    name: str = Form(None),
    description: str = Form(None),
    quantity: int = Form(None),
    purchase_price: float = Form(None),
    sale_price: float = Form(None),
    low_stock_threshold: int = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if name is not None:
        product.name = name
    if description is not None:
        product.description = description
    if quantity is not None:
        product.quantity = quantity
    if purchase_price is not None:
        product.purchase_price = purchase_price
    if sale_price is not None:
        product.sale_price = sale_price
    if low_stock_threshold is not None:
        product.low_stock_threshold = low_stock_threshold
    if image and image.filename:
        product.image_path = _save_image(image)

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}
