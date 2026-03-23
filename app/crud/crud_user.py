
from sqlalchemy.orm import Session
from app.model.user import User
from app.core.security import verify_password

from app.core.security import get_current_user
from fastapi import Depends,HTTPException,status
from app.model.user import UserRole




def get_user_by_email(db: Session,*,email: str):
    N = db.query(User).filter(User.email == email).first()
    return N

def verify_authentication(*,db: Session,email: str,password: str):
    user = get_user_by_email(db = db,email= email)

    if not user:
        return None
    if user.is_deleted:
        return None
    
    password_verify = verify_password(password,user.password)
    if not password_verify:
        return None
    
    return user








def requier_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="admin access requier")
    
    
    return current_user





    


