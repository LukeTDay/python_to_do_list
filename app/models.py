from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship

from . import database
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    todos = relationship("Todo", back_populates="user")


class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(User.id), index=True, nullable=False)
    title = Column(String, nullable=False)
    due_by = Column(DateTime, nullable=False)
    completed = Column(Boolean, default=False)

    user = relationship("User", back_populates="todos")
    
