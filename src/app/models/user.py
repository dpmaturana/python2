
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator

class UserCreate(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: int
    username: str
    is_active: bool


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None

class UserSignup(BaseModel):
    id: int
    username: str
    is_active: bool
    Email: EmailStr
    password: str
    @field_validator('password')
    def password_validator(v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not v.isalnum():
            raise ValueError('Password must be alphanumeric')
        return v