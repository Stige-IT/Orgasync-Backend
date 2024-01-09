from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from core.database import Base


class LogBookActivity(Base):
    __tablename__ = "logbook_activity"

    id = Column(String(100), primary_key=True, autoincrement=False)
    id_logbook = Column(
        String(100), ForeignKey("logbook.id", ondelete="cascade"), nullable=False
    )
    logbook = relationship("LogBook")
    id_logbook_employee = Column(
        String(100),
        ForeignKey("logbook_employee.id", ondelete="cascade"),
        nullable=False,
    )
    employee = relationship("LogBookEmployee")
    description = Column(String(255), nullable=False)
    rating = Column(Integer, nullable=False)
    image = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now())
