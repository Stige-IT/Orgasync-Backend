from typing import Optional
from pydantic import BaseModel


class CompanyRequest(BaseModel):
    name: str
    type: Optional[str]
    size: Optional[int]
