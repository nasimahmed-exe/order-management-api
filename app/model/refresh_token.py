from app.db.base import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Integer,String,ForeignKey,Float,Boolean,func
from datetime import datetime
from sqlalchemy import DateTime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.model.user import User


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,index=True)
    refresh_token: Mapped[str] = mapped_column(String,unique=True,nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    expired_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False)
    is_revoked: Mapped[bool] = mapped_column(Boolean,default=False)
    create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    user: Mapped["User"] = relationship("User",back_populates="refresh_tokens")
