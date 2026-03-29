import json
from fastapi import APIRouter, Depends, HTTPException, Header, status,Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session,selectinload,joinedload
from app.api import deps
from app.schema.order import OrderCreate, OrderRead
from app.crud.crud_order import create_order
from app.crud.crud_idempotency import get_idempotency_key, save_idempotency_record
from fastapi import Request
from app.model.order import Order
from app.model.user import User

from app.core.limiter import limiter
router = APIRouter()

@router.post("/",response_model = OrderRead,status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
def checkout(*,request: Request,db: Session = Depends(deps.get_db),
                       idempotency_key: str = Header(...,alias="Idempotency-Key"),
                       order_in: OrderCreate):
    
    
    
    existing = get_idempotency_key(db,key = idempotency_key,user_id =  order_in.user_id)
    if existing:
        return JSONResponse(
            status_code = existing.status_code,
            content= json.loads(existing.response_snapshot)
        )
    try:


        
        new_order = create_order(db,obj_in=order_in)
        response_data = {
            "id": new_order.id,
            "user_id": new_order.user_id,
            "total_price": new_order.total_price,
            "billing_address": new_order.billing_address,
            "shipping_address": new_order.shipping_address,
        }

        save_idempotency_record(db,key = idempotency_key,user_id=order_in.user_id,
                                order_id=new_order.id,response_snapshot=response_data,
                                status_code=201)
        
        db.commit()
        return JSONResponse(
            status_code= status.HTTP_201_CREATED,
            content= response_data
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected erorr occured during checkout"
        )





@router.get("/selectinload")
def selectinload_check(
                       skip: int = Query(default = 0,ge = 0),
                       limit: int = Query(default = 20, ge = 1, le = 100),
                       db: Session = Depends(deps.get_db)):
    total_order_count = db.query(Order).count()
    orders = db.query(Order).options(selectinload(Order.items)).offset(skip).limit(limit).all()

    return {
        "total_count": total_order_count,
        "skip": skip,
        "limit": limit,
        "has_more": skip + limit < total_order_count,
        "data": orders
    }
     







            

        
                       
        


    


    
        
          








    

     
    
    
    














