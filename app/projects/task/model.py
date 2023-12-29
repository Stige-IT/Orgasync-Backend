from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base
from app.projects.status.model import *
from app.projects.priotity.model import *


class Task(Base):
    __tablename__ = "task"
    id = Column(String(100), primary_key=True, autoincrement=False)
    id_employee_project = Column(
        String(100), ForeignKey("employee_company_project.id", ondelete="CASCADE")
    )
    assignee = relationship("EmployeeCompanyProject", backref="task")
    id_project = Column(String(100), ForeignKey("project.id", ondelete="CASCADE"))
    project = relationship("Project", backref="task")
    name = Column(String(100))
    description = Column(String(100), nullable=True)
    id_status = Column(
        String(100),
        ForeignKey("status.id"),
        nullable=True,
        default="7b564147-3c71-4608-9275-a08b533402a1",
    )
    status = relationship("Status", backref="task")
    id_priority = Column(String(100), ForeignKey("priority.id"), nullable=True)
    priority = relationship("Priority", backref="task")
    created_at = Column(DateTime, default=datetime.now())
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, onupdate=datetime.now)
