from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class ProductBase(BaseModel):
   
    name: str = Field(..., min_length=1, max_length=255, example="Wireless Mouse")
    description: str | None = Field(None, example="A high-precision optical wireless mouse.")
    price: float = Field(..., gt=0, description="Price must be greater than zero")
    stock_quantity: int = Field(0, ge=0, description="Stock cannot be negative")

class ProductCreate(ProductBase):
    
    pass

class ProductRead(ProductBase):
   
    id: int
    is_available: bool

    model_config = ConfigDict(from_attributes=True)
    



