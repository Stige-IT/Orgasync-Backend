import uuid
from datetime import datetime

from sqlalchemy.orm import deferred, relationship

from core.database import Base
from sqlalchemy import Column, Integer, String, DateTime, func, TEXT, Boolean, ForeignKey


class Company(Base):
    __tablename__ = "company"
    id = Column(String(100), primary_key=True, autoincrement=False)
    token_google = Column(TEXT, nullable=True)
    name = Column(String(100))
    email = Column(String(100))
    logo = Column(TEXT)
    cover = Column(TEXT)
    password = deferred(Column(String(100)))
    code = Column(String(6))
    type = Column(String(100))
    size = Column(Integer)
    employees = relationship("Employee", back_populates="company")
    id_address = Column(String(100), ForeignKey("address.id"), nullable=True)
    address = relationship("Address", backref="company", lazy="joined")
    is_active = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True, default=None)
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
