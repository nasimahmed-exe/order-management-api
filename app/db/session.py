from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# The Engine: Connects to the DB hardware
engine = create_engine("postgresql://user:password@db:5432/employee_db", pool_pre_ping=True)

# The Factory: Creates a new 'db' instance for every request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)