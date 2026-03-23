import secrets
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.model.refresh_token import RefreshToken
from app.model.refresh_token import RefreshToken


REFRESH_TOKEN_EXPIRE_DAY = 7

def create_refresh_token(db: Session,*,user_id: int):
    token = secrets.token_hex(32)
    expire_time = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAY  )

    db_add_token = RefreshToken(
        user_id = user_id,
        refresh_token = token,
        expired_at = expire_time,
        is_revoked = False
        
        
    ) 

    db.add(db_add_token)
    return token

def verify_refresh_token(db: Session,*,token: str):
    db_token = db.query(RefreshToken).filter(RefreshToken.refresh_token == token,
                                             RefreshToken.is_revoked == False).first()
    
    if not db_token:
        return None
    if datetime.now(timezone.utc)> db_token.expired_at:
        return None
    
    return db_token


def revoked_refresh_token(db: Session,token: str):
    db_token = db.query(RefreshToken).filter(RefreshToken.refresh_token == token).first()
    if db_token:
        db_token.is_revoked == True
        db.commit()

    

    








