from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# The Engine: Connects to the DB hardware
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
    
)

# The Factory: Creates a new 'db' instance for every request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
