
from fastapi import APIRouter, Depends, HTTPException, status
import time
import asyncio
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api import deps
from app.schema.auth import LoginRequest,LoginResponse,refreshTokenRequest
from app.crud.crud_user import get_user_by_email,verify_authentication
from app.core.security import create_access_token
from app.model.user import User
from app.core.security import get_current_user
from app.crud.crud_refresh_token import create_refresh_token,verify_refresh_token,revoked_refresh_token
import logging
import logging
from fastapi import Request
from app.core.limiter import limiter
logger = logging.getLogger(__name__)


router = APIRouter()

@router.post("/login",response_model = LoginResponse,status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def login(*,request: Request,db: Session = Depends(deps.get_db),obj_in:OAuth2PasswordRequestForm=Depends()):

    correlation_id = request.state.correlation_id
    logger.info(
        "login attemp",
        extra={
            "correlation_id": correlation_id,
            "endpoint": "/auth/login" 
        }
    )
    
    
    
    user = verify_authentication(db = db,email = obj_in.username,password=obj_in.password)
    
    if not user:
        logger.warning(
            "login failed",
            extra= {
                "correlation_id": correlation_id,
                "endpoint": "/auth/login"
            }
        )
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
        )

    
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(db = db,user_id= user.id)
    db.commit()
    logger.info(
        "login succesfully",
        extra= {
            "correlation_id": correlation_id ,
            "user_id": user.id,
            "endpoint": "/auth/login"
        }
    )
    
    return LoginResponse(access_token = access_token,
                         refresh_token = refresh_token)




@router.post("/refresh")
def refresh(*,db: Session = Depends(deps.get_db),db_obj:refreshTokenRequest):
    verify = verify_refresh_token(db,token = db_obj.refresh_token )
    if not verify:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                            detail="invalid token or expire token")
    
    new_access_token = create_access_token(data={"sub": str(verify.user_id)})
    return {"access_token": new_access_token}



@router.post("/logout")
def revoked_token(*,db: Session = Depends(deps.get_db),db_ob: refreshTokenRequest):
    revoked_refresh_token(db = db,token=db_ob.refresh_token)
    return {"message": "succesfully logout"}






@router.post("/profile")
def create_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email
    }

import time
import asyncio

@router.get("/slow-test")
async def slow_endpoint():
    await asyncio.sleep(10)
    return {"message": "finally done"}
    


    


    