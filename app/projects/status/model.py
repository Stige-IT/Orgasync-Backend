from sqlalchemy import Boolean, Column, Integer, String, ForeignKey

from core.database import Base


class Status(Base):
    __tablename__ = "status"
    id = Column(String(100), primary_key=True, autoincrement=False)
    name = Column(String(100))
    color = Column(String(100))
    level = Column(Integer, default=False)
