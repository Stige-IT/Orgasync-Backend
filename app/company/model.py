import uuid
from datetime import datetime

from sqlalchemy.orm import deferred, relationship

from core.database import Base
from sqlalchemy import Column, Integer, String, TEXT, ForeignKey


class Company(Base):
    __tablename__ = "company"
    id = Column(String(100), primary_key=True, autoincrement=False)
    id_user = Column(String(100), ForeignKey("users.id"))
    owner = relationship("UserModel", backref="company", lazy="joined")
    name = Column(String(100))
    logo = Column(TEXT, nullable=True)
    code = Column(String(100), nullable=True)
    size = Column(Integer, nullable=True)
    cover = Column(TEXT, nullable=True)
    description = Column(String(255), nullable=True)
    id_type_company = Column(String(100), ForeignKey("type_company.id"), nullable=True)
    type_company = relationship("TypeCompany", backref="company", lazy="joined")
    employees = relationship("Employee", cascade="all, delete-orphan")
