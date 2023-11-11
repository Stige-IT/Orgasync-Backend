from pydantic import BaseModel


class CompanyRequest(BaseModel):
    name: str
    email: str
    password: str
    type: str
    size: int
