from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector
from app.db.base import Base


class Document(Base):
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,index=True)
    title: Mapped[str] = mapped_column(String,nullable=False)
    content: Mapped[str] = mapped_column(Text,nullable=False)
    embedding = Column(Vector(384),nullable=True)