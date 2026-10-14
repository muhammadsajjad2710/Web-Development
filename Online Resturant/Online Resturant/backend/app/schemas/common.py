"""Shared Pydantic schemas."""

from datetime import datetime
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    success: bool = True
    message: str


class PaginatedResponse(BaseModel, Generic[T]):
    success: bool = True
    items: List[T]
    total: int
    page: int
    page_size: int
    pages: int


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TimestampSchema(ORMModel):
    created_at: datetime
    updated_at: datetime


class IDSchema(ORMModel):
    id: UUID
