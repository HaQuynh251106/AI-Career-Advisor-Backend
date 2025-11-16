
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    role: str = "job_seeker"

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserRead(UserBase):
    id: str # Beanie sẽ trả về ID dưới dạng string
    role: str
    is_active: bool

    class Config:
        from_attributes = True # Cho phép Pydantic đọc từ ORM model
