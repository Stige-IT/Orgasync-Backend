from typing import List
from pydantic import BaseModel


class EmployeeProjectRequest(BaseModel):
    employee_id: List[str]
