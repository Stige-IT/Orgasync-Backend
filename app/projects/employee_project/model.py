from sqlalchemy import Column, String, ForeignKey

from core.database import Base


class EmployeeProject(Base):
    __tablename__ = "employee_project"
    id = Column(String(100), primary_key=True, autoincrement=False)
    id_project = Column(String(100), ForeignKey("project.id"))
    id_employee = Column(String(100), ForeignKey("employee.id"))
