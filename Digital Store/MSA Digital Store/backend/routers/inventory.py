from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from database import get_db
from models import Inventory, Product, StockStatus, User, UserRole
from schemas import InventoryUpdate, InventoryOut, MessageOut, ProductOut
from auth import require_roles
from routers.products import compute_stock_status

router = APIRouter(prefix="/api/inventory", tags=["Inventory"])


@router.get("", response_model=list[InventoryOut])
def list_inventory(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin, UserRole.seller)),
):
    return (
        db.query(Inventory)
        .options(
            joinedload(Inventory.product).joinedload(Product.images),
            joinedload(Inventory.product).joinedload(Product.category),
            joinedload(Inventory.product).joinedload(Product.seller),
        )
        .all()
    )


@router.get("/low-stock", response_model=list[ProductOut])
def low_stock(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin, UserRole.seller)),
):
    return (
        db.query(Product)
        .options(joinedload(Product.category), joinedload(Product.seller), joinedload(Product.images))
        .filter(Product.stock_status == StockStatus.low_stock, Product.is_active == True)  # noqa: E712
        .all()
    )


@router.get("/out-of-stock", response_model=list[ProductOut])
def out_of_stock(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin, UserRole.seller)),
):
    return (
        db.query(Product)
        .options(joinedload(Product.category), joinedload(Product.seller), joinedload(Product.images))
        .filter(Product.stock_status == StockStatus.out_of_stock, Product.is_active == True)  # noqa: E712
        .all()
    )


@router.get("/warehouse", response_model=list[ProductOut])
def warehouse_products(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin, UserRole.seller)),
):
    return (
        db.query(Product)
        .options(joinedload(Product.category), joinedload(Product.seller), joinedload(Product.images))
        .filter(Product.warehouse_available == True, Product.is_active == True)  # noqa: E712
        .all()
    )


@router.put("/{product_id}", response_model=InventoryOut)
def update_stock(
    product_id: int,
    payload: InventoryUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin, UserRole.seller)),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    inv = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    if not inv:
        inv = Inventory(product_id=product_id, quantity=payload.quantity)
        db.add(inv)

    inv.quantity = payload.quantity
    if payload.low_stock_threshold is not None:
        inv.low_stock_threshold = payload.low_stock_threshold
    if payload.warehouse_location is not None:
        inv.warehouse_location = payload.warehouse_location

    product.stock = payload.quantity
    product.stock_status = compute_stock_status(payload.quantity, inv.low_stock_threshold)
    db.commit()

    return (
        db.query(Inventory)
        .options(
            joinedload(Inventory.product).joinedload(Product.images),
            joinedload(Inventory.product).joinedload(Product.category),
            joinedload(Inventory.product).joinedload(Product.seller),
        )
        .filter(Inventory.product_id == product_id)
        .first()
    )


@router.post("/{product_id}/add", response_model=InventoryOut)
def add_stock(
    product_id: int,
    amount: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin, UserRole.seller)),
):
    if amount < 1:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    inv = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    new_qty = (inv.quantity if inv else product.stock) + amount
    return update_stock(
        product_id=product_id,
        payload=InventoryUpdate(quantity=new_qty),
        db=db,
        _=current_user,
    )
