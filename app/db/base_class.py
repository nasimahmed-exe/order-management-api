# app/db/base_class.py
from typing import Any
from sqlalchemy.orm import DeclarativeBase, declared_attr

class Base(DeclarativeBase):
    id: Any
    __name__: str

    # This auto-generates the table name from the class name
    # Class 'User' -> table 'user'
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()