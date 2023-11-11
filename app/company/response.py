from pydantic import BaseModel


class CompanyResponse(BaseModel):
    id: str
    email: str
    name: str
    code: str
    type: str
    size: int
