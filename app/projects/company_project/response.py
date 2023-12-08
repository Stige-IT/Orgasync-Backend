from datetime import datetime
from typing import Union
from pydantic import BaseModel

from app.company.response import CompanyResponse


class CompanyProjectResponse(BaseModel):
    id: str
    name: str
    description: Union[None, str] = None
    image: Union[None, str] = None
    created_at: datetime
    # company: CompanyResponse

    class Config:
        from_attributes = True
