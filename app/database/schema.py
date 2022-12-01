from sqlalchemy import Column, Integer, DateTime, func, String, ForeignKey
from sqlalchemy.orm import relationship

from .connection import Base


class BaseMixin:
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime,
        nullable=True,
        default=func.now(),
        onupdate=func.now(),
    )


class User(Base, BaseMixin):
    __tablename__ = "users"
    email = Column(String(length=255), nullable=False)
    name = Column(String(length=255), nullable=False)
    password = Column(String(length=255), nullable=False)
    boards = relationship("Board", back_populates="user")


class Board(Base, BaseMixin):
    __tablename__ = "boards"
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(length=255), nullable=False)
    content = Column(String(length=255), nullable=False)
    user = relationship("User", back_populates="boards")
