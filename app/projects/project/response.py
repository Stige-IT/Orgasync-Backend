from datetime import datetime
from pydantic import BaseModel


class ProjectResponse(BaseModel):
    id: str
    name: str
    description: str
    created_at: datetime
    total_task: int
    done: int = 0
    undone: int = 0
    percentase: float = 0.0
    # company_project: CompanyProjectResponse

    class Config:
        from_attributes = True
