from pydantic import BaseModel


class CompanyRequest(BaseModel):
    name: str
    type: str
    size: int
