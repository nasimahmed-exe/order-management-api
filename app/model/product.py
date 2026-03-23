from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Integer,String,ForeignKey,Float,Boolean,CheckConstraint
from app.db.base import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.model.lineItem import LineItem

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,index=True)
    name: Mapped[str] = mapped_column(String,nullable=False)
    description: Mapped[str | None] = mapped_column(String,nullable=True)
    price: Mapped[float] = mapped_column(Float,nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer,default=0)
    is_available: Mapped[bool] = mapped_column(Boolean,default=True)
    _python_table_args_ = (
        CheckConstraint("price > 0",name = "check_price_positive"),
        CheckConstraint("stock_quantity >= 0",name = "check_stock_non_negative")
        
    )

    #Relations:
    line_items: Mapped[list["LineItem"]] = relationship("LineItem",back_populates="product")
