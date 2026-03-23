from pydantic import BaseModel, Field, ConfigDict


class LineItemBase(BaseModel):
  
    product_id: int = Field(..., gt=0, description="The ID of the product being purchased")
    quantity: int = Field(..., ge=1, le=10, description="Quantity must be between 1 and 10")

class LineItemCreate(LineItemBase):
   
    pass

class LineItemRead(LineItemBase):
    
    id: int
    order_id: int
    price: float

    # Enables compatibility with SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)
    
    
