from pydantic import BaseModel


class EmployeeCompanyProjectResponse(BaseModel):
    id: str
    id_employee: str
    id_company_project: str

    class Config:
        from_attributes = True
