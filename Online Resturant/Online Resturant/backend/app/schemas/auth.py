"""Auth and user schemas."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.schemas.common import ORMModel, TimestampSchema, TokenPair


class RoleOut(ORMModel):
    id: UUID
    name: str
    display_name: str


class UserOut(TimestampSchema):
    id: UUID
    email: EmailStr
    phone: Optional[str] = None
    full_name: str
    role: RoleOut
    restaurant_id: Optional[UUID] = None
    is_active: bool
    is_verified: bool
    avatar_url: Optional[str] = None
    last_login_at: Optional[datetime] = None


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=2, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=32)

    @field_validator("password")
    @classmethod
    def password_strength(cls, value: str) -> str:
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one digit")
        if not any(c.isalpha() for c in value):
            raise ValueError("Password must contain at least one letter")
        return value


class RestaurantRegisterRequest(BaseModel):
    # Owner account
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=2, max_length=255)
    phone: Optional[str] = None
    # Restaurant
    restaurant_name: str = Field(min_length=2, max_length=255)
    cuisine_type: Optional[str] = None
    city: Optional[str] = "Lahore"
    country: str = "Pakistan"
    contact_number: Optional[str] = None
    whatsapp_number: Optional[str] = None
    address: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    success: bool = True
    tokens: TokenPair
    user: UserOut


class RefreshRequest(BaseModel):
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8, max_length=128)
