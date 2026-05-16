from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    nickname: str = Field(..., min_length=1, max_length=50)
    email: EmailStr | None = None
    phone: str | None = None
    status: int = 1


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=50)


class UserUpdate(BaseModel):
    nickname: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    status: int | None = None


class UserPasswordUpdate(BaseModel):
    old_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6, max_length=50)


class UserResponse(BaseModel):
    id: int
    username: str
    nickname: str
    email: str | None
    phone: str | None
    status: int
    created_at: datetime

    model_config = {"from_attributes": True}
