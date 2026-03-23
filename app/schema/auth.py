from pydantic import BaseModel,EmailStr,Field

class LoginRequest(BaseModel):
    email: EmailStr = Field(...,)
    password: str = Field(...,)


class refreshTokenRequest(BaseModel):
    refresh_token: str



class LoginResponse(BaseModel):
    access_token : str
    refresh_token : str
    
    token_type : str = "bearer"

