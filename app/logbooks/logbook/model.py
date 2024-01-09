from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from core.database import Base


class LogBook(Base):
    __tablename__ = "logbook"

    id = Column(String(100), primary_key=True, autoincrement=False)
    id_company = Column(String(100), ForeignKey("company.id"), nullable=False)
    company = relationship("Company")
    name = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    periode_start = Column(DateTime)
    periode_end = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now())
