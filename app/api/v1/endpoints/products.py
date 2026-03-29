from fastapi import APIRouter, Depends, status,Query
from sqlalchemy.orm import Session,selectinload
from app.api import deps
from app.schema.product import ProductCreate, ProductRead
from app.model.product import Product
from fastapi import Request
from app.core.limiter import limiter
from app.core.redis import redis_client
import logging
import json
logger = logging.getLogger(__name__)

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


@router.get("/products")
@limiter.limit("100/minute")
def selectinload_and_pagination_check(*,
                                      request: Request,
                                      db: Session = Depends(deps.get_db),
                                      skip: int = Query(default=0,ge = 0),
                                      limit: int = Query(default=20,ge = 1,le = 100)):
    cache_key = f"products:skip = {skip}: limit =  {limit}"

    cached = redis_client.get(cache_key)
    if cached:
        logger.info("Cache hit",extra={"Cache key": cache_key})
        return json.loads(cached)
    
    logger.info("Cache miss",extra={"Cache key": cache_key})

    
    
    products = db.query(Product).offset(skip).limit(limit).all()

    total_count = db.query(Product).count()
    response =  {
        "Total_product_count": total_count,
        "skip": skip,
        "limit": limit,
        "has_more": (skip + limit) < total_count,
        "products":[
            {
                "id":p.id,
                "name":p.name,
                "price": p.price,
                "stock_quantity": p.stock_quantity,
                "is_avilable": p.is_available
            }
            for p in products
        ]
    
    }
    redis_client.setex(cache_key,300,json.dumps(response))
    return response




    