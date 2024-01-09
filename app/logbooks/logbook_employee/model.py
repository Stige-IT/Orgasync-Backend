from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from core.database import Base


class LogBookEmployee(Base):
    __tablename__ = "logbook_employee"

    id = Column(String(100), primary_key=True, autoincrement=False)
    id_logbook = Column(
        String(100), ForeignKey("logbook.id", ondelete="cascade"), nullable=False
    )
    logbook = relationship("LogBook")
    id_employee = Column(String(100), ForeignKey("employee.id"), nullable=False)
    employee = relationship("Employee")
