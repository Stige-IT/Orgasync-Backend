from sqlalchemy import Column, String, ForeignKey

from core.database import Base


class EmployeeProjectTask(Base):
    __tablename__ = "employee_project_task"
    id = Column(String(100), primary_key=True, autoincrement=False)
    id_employee_project = Column(String(100), ForeignKey("employee_project.id"))
