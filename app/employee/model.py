from app.employee.constant import defaultType
from app.position.model import *
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.position.constant import defaulIdPosition
from core.database import Base


class Employee(Base):
    __tablename__ = "employee"
    id = Column(String(100), primary_key=True, autoincrement=False)
    id_user = Column(String(100), ForeignKey("users.id"))
    user = relationship("UserModel")

    id_company = Column(String(100), ForeignKey("company.id"))
    company = relationship("Company")

    id_position = Column(String(100), ForeignKey("position.id"), default=defaulIdPosition)
    position = relationship("Position")

    joined = Column(DateTime, nullable=True, default=datetime.now)
    id_type = Column(String(25), ForeignKey("type_employee.id"), nullable=True, default=defaultType)
    type = relationship("TypeEmployee")
    end = Column(DateTime, nullable=True)


class TypeEmployee(Base):
    __tablename__ = "type_employee"
    id = Column(String(100), primary_key=True, autoincrement=False)
    name = Column(String(25))
