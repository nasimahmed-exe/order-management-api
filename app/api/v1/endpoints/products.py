from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api import deps
from app.schema.product import ProductCreate, ProductRead
from app.model.product import Product
from fastapi import Request
from app.core.limiter import limiter

router = APIRouter()

@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
@limiter.limit("100/minute")
def create_product(*,request: Request,product_in: ProductCreate, db: Session = Depends(deps.get_db)):
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