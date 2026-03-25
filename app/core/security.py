from passlib.context import CryptContext
from datetime import datetime,timedelta


from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.api import deps
from jose import jwt,JWTError
from app.model.user import User
from app.core.config import settings




context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

def hashing_password(password: str)-> str:
    return context.hash(password)

def verify_password(password,hashing_password)-> bool:
    return context.verify(password,hashing_password)




def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire_time = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire_time})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)




    


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(deps.get_db)):

    try:
        token_verify = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])   
        user_id = token_verify.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED
                                ,detail="expired or invalid playloads")
        
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid playload or expired token")


    user = db.query(User).filter(User.id == int(user_id),User.is_deleted == False).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail = "invalid playloads or expired token")
    return user    



    


    




