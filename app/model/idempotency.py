from sqlalchemy import String, Integer, Text, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.db.base_class import Base

class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    idempotency_key: Mapped[str] = mapped_column(
        String(255), 
        nullable=False, 
        unique=True
    )
    
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    
    order_id: Mapped[int] = mapped_column(Integer, nullable=True)
    
    response_snapshot: Mapped[str] = mapped_column(Text, nullable=False)
    
    status_code: Mapped[int] = mapped_column(Integer, nullable=False)
    
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )


     