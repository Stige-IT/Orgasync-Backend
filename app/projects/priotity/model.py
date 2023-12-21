from sqlalchemy import Column, Integer, String
from core.database import Base


class Priority(Base):
    __tablename__ = "priority"
    id = Column(String(100), primary_key=True, autoincrement=False)
    name = Column(String(100))
    level = Column(Integer)
