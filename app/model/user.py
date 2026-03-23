from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Integer,String,ForeignKey,Float,Boolean,DateTime,CheckConstraint
from sqlalchemy import Enum as SAEnum
from enum import Enum
from datetime import datetime

from app.db.base import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.model.order import Order
if TYPE_CHECKING:
    from app.model.refresh_token import RefreshToken


class UserRole(str,Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,index=True)
    name: Mapped[str] = mapped_column(String,nullable=False)
    email: Mapped[str] = mapped_column(String,unique=True,nullable=False,index=True)
    password: Mapped[str] = mapped_column(String,nullable=False)
    phone_number: Mapped[str | None] = mapped_column(String,nullable=True)
    balance: Mapped[float] = mapped_column(Float,default=0.0)
    is_active: Mapped[bool] = mapped_column(Boolean,default=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean,default=False)
    deleted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=True)
    __table_args__ = (
        CheckConstraint( "balance >= 0",name = "check_balance_non_negative"),
        )
    role: Mapped["UserRole"] = mapped_column(SAEnum(UserRole,name = "userrole"),default=UserRole.USER)

    #Relations:

    orders: Mapped[list["Order"]] = relationship("Order",back_populates="user", cascade="all, delete-orphan")
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship("RefreshToken",back_populates="user")

