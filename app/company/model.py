
from datetime import datetime
from core.database import Base
from sqlalchemy import Column, Integer, String, DateTime, func, TEXT


class UserModel(Base):
    __tablename__ = "company"
    id = Column(String(100), primary_key=True, autoincrement=False)
    name = Column(String(100))
    image = Column(TEXT)
    password = Column(String(100))
    code = Column(String(6))
    type = Column(String(100))
    size = Column(Integer)
    id_address = Column(String(100))
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    created_at = Column(DateTime, nullable=False, server_default=func.now())