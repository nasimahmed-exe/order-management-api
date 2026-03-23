from typing import TYPE_CHECKING
from datetime import    datetime
from sqlalchemy import Integer, String, DateTime, func,Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
if TYPE_CHECKING:
    from .lineItem import LineItem
    from .user import User

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True,index=True
        )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False,index=True)
    billing_address: Mapped[str] = mapped_column(String,nullable=False)
    shipping_address: Mapped[str] = mapped_column(
        String , nullable=False
        )
    ordered_at: Mapped[datetime] = mapped_column(
        DateTime, server_default= func.now()
        )
    total_price: Mapped[float] = mapped_column(Float, nullable=False)

    items: Mapped[list["LineItem"]] = relationship(
        "LineItem",cascade="all, delete-orphan", back_populates="order")

    user: Mapped["User"] = relationship("User", back_populates="orders")