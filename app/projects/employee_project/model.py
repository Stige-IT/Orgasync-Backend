from app.projects.project.model import *
from app.employee.model import *

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base


class EmployeeCompanyProject(Base):
    __tablename__ = "employee_project"
    id = Column(String(100), primary_key=True, autoincrement=False)
    id_project = Column(String(100), ForeignKey("project.id"))
    project = relationship("Project", backref="employee_project", lazy="joined")
    id_employee = Column(String(100), ForeignKey("employee.id"))
    employee = relationship("Employee", backref="employee_project", lazy="joined")
