import datetime
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from core.database import Base


class EmployeeCompanyProject(Base):
    __tablename__ = "employee_company_project"
    id = Column(String(100), primary_key=True, autoincrement=False)
    id_employee = Column(String(100), ForeignKey("employee.id"))
    employee = relationship("Employee")
    id_company_project = Column(String(100), ForeignKey("company_project.id"))
    company_project = relationship("CompanyProject")
    joined = Column(DateTime, default=datetime.datetime.now)
