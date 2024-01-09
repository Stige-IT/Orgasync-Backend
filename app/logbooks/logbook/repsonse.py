from datetime import datetime
from typing import Union
from pydantic import BaseModel

from app.company.response import CompanyResponse


class LogBookResponse(BaseModel):
    id: str
    name: Union[str, None] = None
    description: Union[str, None] = None
    periode_start: datetime
    periode_end: datetime
    created_at: datetime
    company: CompanyResponse

    class Config:
        from_attributes = True
