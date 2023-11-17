from pydantic import BaseModel


class CompanyProjectResponse(BaseModel):
    id: str
    id_company: str
    name: str

    class Config:
        from_attributes = True
