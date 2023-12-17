from datetime import datetime
from pydantic import BaseModel


class ProjectResponse(BaseModel):
    id: str
    name: str
    description: str
    created_at: datetime
    # company_project: CompanyProjectResponse

    class Config:
        from_attributes = True
