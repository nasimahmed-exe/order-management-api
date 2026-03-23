from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api import deps
from app.schema.product import ProductCreate, ProductRead
from app.model.product import Product

router = APIRouter()

@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(product_in: ProductCreate, db: Session = Depends(deps.get_db)):
    db_product = Product(
        name=product_in.name,
        description=product_in.description,
        price=product_in.price,
        stock_quantity=product_in.stock_quantity,
        is_available=True
    )
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product