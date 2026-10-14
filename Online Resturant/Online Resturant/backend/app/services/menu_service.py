"""Menu management service."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from app.core.exceptions import NotFoundError
from app.models.menu import Category, ItemAddon, ItemVariation, MenuItem
from app.schemas.menu import CategoryCreate, CategoryUpdate, MenuItemCreate, MenuItemUpdate
from app.utils.helpers import unique_slug


class MenuService:
    def __init__(self, db: Session):
        self.db = db

    # Categories
    def list_categories(self, restaurant_id: UUID) -> List[Category]:
        return (
            self.db.query(Category)
            .filter(Category.restaurant_id == restaurant_id, Category.is_deleted.is_(False))
            .order_by(Category.sort_order, Category.name)
            .all()
        )

    def create_category(self, restaurant_id: UUID, data: CategoryCreate) -> Category:
        slug = unique_slug(
            data.name,
            lambda s: self.db.query(Category)
            .filter(Category.restaurant_id == restaurant_id, Category.slug == s)
            .first()
            is not None,
        )
        category = Category(
            restaurant_id=restaurant_id,
            slug=slug,
            **data.model_dump(),
        )
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update_category(
        self, restaurant_id: UUID, category_id: UUID, data: CategoryUpdate
    ) -> Category:
        category = self._get_category(restaurant_id, category_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(category, key, value)
        self.db.commit()
        self.db.refresh(category)
        return category

    def _get_category(self, restaurant_id: UUID, category_id: UUID) -> Category:
        category = (
            self.db.query(Category)
            .filter(
                Category.id == category_id,
                Category.restaurant_id == restaurant_id,
                Category.is_deleted.is_(False),
            )
            .first()
        )
        if not category:
            raise NotFoundError("Category not found")
        return category

    # Items
    def list_items(
        self,
        restaurant_id: UUID,
        category_id: Optional[UUID] = None,
        search: Optional[str] = None,
        available_only: bool = False,
    ) -> List[MenuItem]:
        query = (
            self.db.query(MenuItem)
            .options(joinedload(MenuItem.variations), joinedload(MenuItem.addons))
            .filter(MenuItem.restaurant_id == restaurant_id, MenuItem.is_deleted.is_(False))
        )
        if category_id:
            query = query.filter(MenuItem.category_id == category_id)
        if available_only:
            query = query.filter(MenuItem.is_available.is_(True))
        if search:
            like = f"%{search}%"
            query = query.filter(MenuItem.name.ilike(like))
        return query.order_by(MenuItem.sort_order, MenuItem.name).all()

    def get_item(self, restaurant_id: UUID, item_id: UUID) -> MenuItem:
        item = (
            self.db.query(MenuItem)
            .options(joinedload(MenuItem.variations), joinedload(MenuItem.addons))
            .filter(
                MenuItem.id == item_id,
                MenuItem.restaurant_id == restaurant_id,
                MenuItem.is_deleted.is_(False),
            )
            .first()
        )
        if not item:
            raise NotFoundError("Menu item not found")
        return item

    def create_item(self, restaurant_id: UUID, data: MenuItemCreate) -> MenuItem:
        slug = unique_slug(
            data.name,
            lambda s: self.db.query(MenuItem)
            .filter(MenuItem.restaurant_id == restaurant_id, MenuItem.slug == s)
            .first()
            is not None,
        )
        payload = data.model_dump(exclude={"variations", "addons"})
        item = MenuItem(restaurant_id=restaurant_id, slug=slug, **payload)
        self.db.add(item)
        self.db.flush()

        for variation in data.variations:
            self.db.add(ItemVariation(menu_item_id=item.id, **variation.model_dump()))
        for addon in data.addons:
            self.db.add(ItemAddon(menu_item_id=item.id, **addon.model_dump()))

        self.db.commit()
        return self.get_item(restaurant_id, item.id)

    def update_item(self, restaurant_id: UUID, item_id: UUID, data: MenuItemUpdate) -> MenuItem:
        item = self.get_item(restaurant_id, item_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(item, key, value)
        self.db.commit()
        return self.get_item(restaurant_id, item_id)

    def soft_delete_item(self, restaurant_id: UUID, item_id: UUID) -> None:
        from datetime import datetime, timezone

        item = self.get_item(restaurant_id, item_id)
        item.is_deleted = True
        item.deleted_at = datetime.now(timezone.utc)
        item.is_available = False
        self.db.commit()
