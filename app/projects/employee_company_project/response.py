from pydantic import BaseModel
from app.employee.model import *
from app.employee.response import EmployeesCompanyResponse


class EmployeeCompanyProjectResponse(BaseModel):
    id: str
    employee: EmployeesCompanyResponse

    class Config:
        from_attributes = True
