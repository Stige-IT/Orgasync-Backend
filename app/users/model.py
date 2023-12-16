import app.address.model
from datetime import datetime

from sqlalchemy.orm import deferred, relationship

from app.users.enums import RoleUser
from core.database import Base
from sqlalchemy import Column, String, Boolean, DateTime, func, Text, TEXT, ForeignKey


class Role(Base):
    __tablename__ = "role"
    id = Column(String(100), primary_key=True, autoincrement=False)
    name = Column(String(100))


class UserModel(Base):
    __tablename__ = "users"
    id = Column(String(100), primary_key=True, autoincrement=False)
    token_google = Column(TEXT, nullable=True)
    name = Column(String(100))
    gender = Column(String(10))
    image = Column(Text)
    email = Column(String(255), unique=True)
    password = deferred(Column(String(100)))
    id_address = Column(String(100), ForeignKey("address.id"), nullable=True)
    address = relationship("Address", backref="users", lazy="joined")
    is_active = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True, default=None)
    registered_at = Column(DateTime, nullable=True, default=None)
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    id_role = Column(String(100), ForeignKey("role.id"), nullable=True, default=RoleUser.USER.value)
    role = relationship("Role", backref="users", lazy="joined")
