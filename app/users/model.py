from datetime import datetime

from sqlalchemy.orm import deferred, relationship

from core.database import Base
from sqlalchemy import Column, String, Boolean, DateTime, func, Text, TEXT


class UserModel(Base):
    __tablename__ = "users"
    id = Column(String(100), primary_key=True, autoincrement=False)
    token_google = Column(TEXT, nullable=True)
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
    employee = relationship("Employee", back_populates="user")
