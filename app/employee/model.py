from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base


class Employee(Base):
    __tablename__ = "employee"
    id = Column(String(100), primary_key=True, autoincrement=False)
    id_user = Column(String(100), ForeignKey("users.id"))
    user = relationship("UserModel")

    id_company = Column(String(100), ForeignKey("company.id"))
    company = relationship("Company", back_populates="employees")

    joined = Column(DateTime, nullable=True, default=datetime.now)
    type = Column(String(25), nullable=True, default="guest")
    end = Column(DateTime, nullable=True)


class TypeEmployee(Base):
    __tablename__ = "type_employee"
    id = Column(String(100), primary_key=True, autoincrement=False)
    name = Column(String(25))
