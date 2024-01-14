from datetime import datetime
from typing import List, Union
from pydantic import BaseModel

from app.company.response import CompanyResponse
from app.projects.employee_company_project.response import (
    EmployeeCompanyProjectResponse,
)
from app.projects.project.response import ProjectResponse


class CompanyProjectResponse(BaseModel):
    id: str
    name: str
    description: Union[None, str] = None
    image: Union[None, str] = None
    created_at: datetime
    # company: CompanyResponse

    class Config:
        from_attributes = True


class CompanyProjectResult(BaseModel):
    company_project: CompanyProjectResponse
    total_employee: Union[None, int] = 0
    # employee: List[EmployeeCompanyProjectResponse] = []
    total_project: Union[None, int] = 0
    # project: List[ProjectResponse] = []

    class Config:
        from_attributes = True
