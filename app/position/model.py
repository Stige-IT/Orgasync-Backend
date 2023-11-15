from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from core.database import Base


class Position(Base):
    __tablename__ = "position"
    id = Column(String(100), primary_key=True, autoincrement=False)
    name = Column(String(100))
    employee = relationship("Employee", back_populates="position")

