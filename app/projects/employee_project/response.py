from pydantic import BaseModel

from app.projects.company_project.response import CompanyProjectResponse
from app.projects.project.response import ProjectResponse


class EmployeeProjectResponse(BaseModel):
    id: str
    project: ProjectResponse

    class Config:
        from_attributes = True
