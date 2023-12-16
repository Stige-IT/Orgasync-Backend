from typing import List, Optional
from fastapi import UploadFile
from pydantic import BaseModel


class EmployeeProjectRequest(BaseModel):
    employee_id: List[str]


class CompanyProjectRequest(BaseModel):
    name: str
    description: Optional[str] = None
