from fastapi import FastAPI
from fastapi.exceptions import HTTPException,RequestValidationError
from app.db.base import Base
from app.db.session import engine
from app.api.v1 import api
from app.core.logging_config import setup_logging
from app.middleware.correlation import CorrelationIDMiddleware
from app.core.error_handlers import (
    http_exception_error_handler,
    validation_error_handler,
    unexpected_exception_error_handler
)

from slowapi import _rate_limit_exceeded_handler
from app.core.limiter import limiter
from slowapi.errors import RateLimitExceeded



Base.metadata.create_all(bind=engine)
setup_logging()





app = FastAPI()
app.add_middleware(CorrelationIDMiddleware)
app.add_exception_handler(HTTPException,http_exception_error_handler)
app.add_exception_handler(RequestValidationError,validation_error_handler)
app.add_exception_handler(Exception,unexpected_exception_error_handler)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler)




app.include_router(api.api_router,prefix="/api/v1")
@app.get("/")
def home():
    return {"message": "API is running. Visit /docs for the swagger UI."}































