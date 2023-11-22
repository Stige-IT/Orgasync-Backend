from pydantic import BaseModel

from app.projects.company_project.response import CompanyProjectResponse


class ProjectResponse(BaseModel):
    id: str
    name: str
    description: str
    company_project: CompanyProjectResponse

    class Config:
        from_attributes = True
