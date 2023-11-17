from sqlalchemy import Column, String, ForeignKey

from core.database import Base


class Task(Base):
    __tablename__ = "task"
    id = Column(String(100), primary_key=True, autoincrement=False)
    id_employe_project_task = Column(String(100), ForeignKey("employee_project_task.id"))
    name = Column(String(100))
    description = Column(String(100), nullable=True)
    status = Column(String(100), ForeignKey("status.id"))
