from pydantic import BaseModel


class EmployeeCreateRequest(BaseModel):
    id_company: str
    id_user: str
    type: str