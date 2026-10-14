from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from database import get_db
from models import (
    Product,
    ProductImage,
    Inventory,
    Category,
    StockStatus,
    User,
    UserRole,
    ProductBadge,
)
from schemas import ProductCreate, ProductUpdate, ProductOut, MessageOut
from auth import require_roles

router = APIRouter(prefix="/api/products", tags=["Products"])


def compute_stock_status(stock: int, threshold: int = 10) -> StockStatus:
    if stock <= 0:
        return StockStatus.out_of_stock
    if stock <= threshold:
        return StockStatus.low_stock
    return StockStatus.in_stock


def slugify(text: str) -> str:
    return (
        text.lower()
        .strip()
        .replace("&", "and")
        .replace(" ", "-")
        .replace("/", "-")
    )


def product_query(db: Session):
    return db.query(Product).options(
        joinedload(Product.category),
        joinedload(Product.seller),
        joinedload(Product.images),
    )


@router.get("", response_model=list[ProductOut])
def list_products(
    q: str | None = None,
    category: str | None = None,
    category_id: int | None = None,
    seller_id: int | None = None,
    badge: ProductBadge | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = product_query(db).filter(Product.is_active == True)  # noqa: E712

    if q:
        like = f"%{q}%"
        query = query.filter(or_(Product.name.ilike(like), Product.description.ilike(like)))
    if category:
        query = query.join(Category).filter(or_(Category.slug == category, Category.name == category))
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if seller_id:
        query = query.filter(Product.seller_id == seller_id)
    if badge:
        query = query.filter(Product.badge == badge)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    return query.order_by(Product.id).offset(skip).limit(limit).all()


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = product_query(db).filter(Product.id == product_id).first()
    if not product:
        # try slug
        product = product_query(db).filter(Product.slug == str(product_id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("", response_model=ProductOut, status_code=201)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin, UserRole.seller)),
):
    slug = payload.slug or slugify(payload.name)
    if db.query(Product).filter(Product.slug == slug).first():
        slug = f"{slug}-{int(__import__('time').time())}"

    stock_status = compute_stock_status(payload.stock)
    product = Product(
        name=payload.name,
        slug=slug,
        description=payload.description,
        features=payload.features,
        price=payload.price,
        original_price=payload.original_price,
        badge=payload.badge,
        stock=payload.stock,
        stock_status=stock_status,
        warehouse_available=payload.warehouse_available,
        category_id=payload.category_id,
        seller_id=payload.seller_id,
        delivery_info=payload.delivery_info or "Delivery within 2–4 working days across Khushab district.",
        return_policy=payload.return_policy or "7-day easy return on unused sealed items.",
    )
    db.add(product)
    db.flush()

    image_url = payload.image_url or f"https://picsum.photos/seed/msa{product.id}/600/600"
    db.add(ProductImage(product_id=product.id, url=image_url, is_primary=True, alt_text=product.name))
    db.add(
        Inventory(
            product_id=product.id,
            quantity=payload.stock,
            low_stock_threshold=10,
            warehouse_location="MSA Warehouse Quaidabad" if payload.warehouse_available else None,
        )
    )
    db.commit()
    return product_query(db).filter(Product.id == product.id).first()


@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin, UserRole.seller)),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    data = payload.model_dump(exclude_unset=True)
    image_url = data.pop("image_url", None)

    for key, value in data.items():
        setattr(product, key, value)

    if "stock" in data:
        inv = db.query(Inventory).filter(Inventory.product_id == product.id).first()
        threshold = inv.low_stock_threshold if inv else 10
        product.stock_status = compute_stock_status(product.stock, threshold)
        if inv:
            inv.quantity = product.stock

    if image_url:
        primary = db.query(ProductImage).filter(ProductImage.product_id == product.id, ProductImage.is_primary == True).first()  # noqa: E712
        if primary:
            primary.url = image_url
        else:
            db.add(ProductImage(product_id=product.id, url=image_url, is_primary=True))

    db.commit()
    return product_query(db).filter(Product.id == product_id).first()


@router.delete("/{product_id}", response_model=MessageOut)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin)),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.is_active = False
    db.commit()
    return {"message": "Product deactivated"}
