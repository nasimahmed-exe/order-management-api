from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from app.model.user import UserRole


class UserBase(BaseModel):
    
    name: str = Field(..., min_length=2, max_length=100, example="John Doe")
    email: EmailStr = Field(..., example="john.doe@example.com")
    role: str = Field(...,)
    # Using 'str | None' to match your SQLAlchemy model 'Mapped[str | None]'
    phone_number: str | None = Field(None, pattern=r"^\+?1?\d{9,15}$", example="+1234567890")

class UserCreate(UserBase):
    password: str = Field(...,)
    

class UserRead(UserBase):
    
    id: int
    balance: float
    is_active: bool

    
    model_config = ConfigDict(from_attributes=True)
    
    




    
