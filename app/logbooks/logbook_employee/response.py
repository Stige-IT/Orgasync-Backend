from pydantic import BaseModel

from app.employee.response import EmployeesCompanyResponse


class LogBookEmployeeResponse(BaseModel):
    id: str
    id_logbook: str
    total_activity: int
    employee: EmployeesCompanyResponse

    class Config:
        from_attributes = True
