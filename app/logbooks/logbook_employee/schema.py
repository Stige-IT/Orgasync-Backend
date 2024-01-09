from typing import List, Optional
from pydantic import BaseModel


class LogbookEmployeeRequest(BaseModel):
    id_employees: Optional[List[str]] = []
