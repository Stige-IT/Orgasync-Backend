from pydantic import BaseModel

from app.company.response import CompanyResponse


class CompanyProjectResponse(BaseModel):
    id: str
    name: str
    company: CompanyResponse

    class Config:
        from_attributes = True
