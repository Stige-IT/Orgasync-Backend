from pydantic import BaseModel


class EmployeeCreateRequest(BaseModel):
    id_user: str
    type: str