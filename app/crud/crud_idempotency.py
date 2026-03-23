import json
from sqlalchemy.orm import Session
from app.model.idempotency import IdempotencyKey

def get_idempotency_key(db: Session,*,key: str,user_id: int):
    a = db.query(IdempotencyKey).filter(
        IdempotencyKey.idempotency_key == key,
        IdempotencyKey.user_id == user_id
    ).first()
    return a



def save_idempotency_record(db: Session,*,key: str,user_id: int,order_id: int,
                            response_snapshot:dict,status_code: int ):
    
    record = IdempotencyKey(
        idempotency_key = key,
        user_id = user_id,
        order_id = order_id,
        response_snapshot = json.dumps(response_snapshot),
        status_code = status_code
        
        
    )
    db.add(record)

    
    

