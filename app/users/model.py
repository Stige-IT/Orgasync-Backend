from datetime import datetime

from sqlalchemy.orm import deferred

from core.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Text


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(100))
    image = Column(Text)
    email = Column(String(255), unique=True)
    password = deferred(Column(String(100)))
    is_active = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True, default=None)
    registered_at = Column(DateTime, nullable=True, default=None)
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
