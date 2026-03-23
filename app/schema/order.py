from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List
# We import these to use them for nesting inside our Order schemas
from .lineItem import LineItemCreate, LineItemRead


class OrderBase(BaseModel):
 
    billing_address: str = Field(..., min_length=5, example="123 Tech Lane, NY")
    shipping_address: str = Field(..., min_length=5, example="123 Tech Lane, NY")
    user_id: int = Field(..., gt=0)

class OrderCreate(OrderBase):
    
    # We call this 'items' to match the relationship name in your Order model
    items: List[LineItemCreate] = Field(..., min_length=1, description="Order must have at least one item")

class OrderRead(OrderBase):
   
    id: int
    total_price: float
    ordered_at: datetime
    # We use LineItemRead here because it includes the ID and the price snapshot
    items: List[LineItemRead]

    model_config = ConfigDict(from_attributes=True)







    
