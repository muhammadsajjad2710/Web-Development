"""Restaurant and branch services."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.branch import Branch
from app.models.restaurant import Restaurant
from app.schemas.restaurant import BranchCreate, BranchUpdate, RestaurantUpdate
from app.utils.helpers import unique_slug


class RestaurantService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, restaurant_id: UUID) -> Restaurant:
        restaurant = (
            self.db.query(Restaurant)
            .filter(Restaurant.id == restaurant_id, Restaurant.is_deleted.is_(False))
            .first()
        )
        if not restaurant:
            raise NotFoundError("Restaurant not found")
        return restaurant

    def get_by_slug(self, slug: str) -> Restaurant:
        restaurant = (
            self.db.query(Restaurant)
            .filter(Restaurant.slug == slug, Restaurant.is_deleted.is_(False))
            .first()
        )
        if not restaurant:
            raise NotFoundError("Restaurant not found")
        return restaurant

    def update(self, restaurant_id: UUID, data: RestaurantUpdate) -> Restaurant:
        restaurant = self.get_by_id(restaurant_id)
        payload = data.model_dump(exclude_unset=True)
        if "name" in payload and payload["name"] != restaurant.name:
            payload["slug"] = unique_slug(
                payload["name"],
                lambda s: self.db.query(Restaurant)
                .filter(Restaurant.slug == s, Restaurant.id != restaurant_id)
                .first()
                is not None,
            )
        for key, value in payload.items():
            setattr(restaurant, key, value)
        self.db.commit()
        self.db.refresh(restaurant)
        return restaurant


class BranchService:
    def __init__(self, db: Session):
        self.db = db

    def list(self, restaurant_id: UUID) -> List[Branch]:
        return (
            self.db.query(Branch)
            .filter(Branch.restaurant_id == restaurant_id, Branch.is_deleted.is_(False))
            .order_by(Branch.is_default.desc(), Branch.name)
            .all()
        )

    def get(self, restaurant_id: UUID, branch_id: UUID) -> Branch:
        branch = (
            self.db.query(Branch)
            .filter(
                Branch.id == branch_id,
                Branch.restaurant_id == restaurant_id,
                Branch.is_deleted.is_(False),
            )
            .first()
        )
        if not branch:
            raise NotFoundError("Branch not found")
        return branch

    def create(self, restaurant_id: UUID, data: BranchCreate) -> Branch:
        branch = Branch(restaurant_id=restaurant_id, **data.model_dump())
        if branch.is_default:
            self._clear_default(restaurant_id)
        self.db.add(branch)
        self.db.commit()
        self.db.refresh(branch)
        return branch

    def update(self, restaurant_id: UUID, branch_id: UUID, data: BranchUpdate) -> Branch:
        branch = self.get(restaurant_id, branch_id)
        payload = data.model_dump(exclude_unset=True)
        if payload.get("is_default"):
            self._clear_default(restaurant_id)
        for key, value in payload.items():
            setattr(branch, key, value)
        self.db.commit()
        self.db.refresh(branch)
        return branch

    def soft_delete(self, restaurant_id: UUID, branch_id: UUID) -> None:
        from datetime import datetime, timezone

        branch = self.get(restaurant_id, branch_id)
        branch.is_deleted = True
        branch.deleted_at = datetime.now(timezone.utc)
        branch.status = "inactive"
        self.db.commit()

    def _clear_default(self, restaurant_id: UUID) -> None:
        self.db.query(Branch).filter(
            Branch.restaurant_id == restaurant_id, Branch.is_default.is_(True)
        ).update({"is_default": False})
