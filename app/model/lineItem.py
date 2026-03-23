from datetime import    datetime
from sqlalchemy import Integer, String, DateTime, func,ForeignKey,Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.model.order import Order
if TYPE_CHECKING:
    from app.model.product import Product

class LineItem(Base):
    __tablename__ = "lineitems"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,index=True)
    price: Mapped[float] = mapped_column(Float,nullable=False)
    quantity: Mapped[int] = mapped_column(Integer,nullable=False)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"),nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    #Relations:
    order: Mapped["Order"] = relationship("Order",back_populates="items") 
    product: Mapped["Product"] = relationship("Product",back_populates="line_items")