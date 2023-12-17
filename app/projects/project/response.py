from pydantic import BaseModel


class ProjectResponse(BaseModel):
    id: str
    name: str
    description: str
    # company_project: CompanyProjectResponse

    class Config:
        from_attributes = True
