from typing import List, Optional
from fastapi import UploadFile
from pydantic import BaseModel


class CompanyProjectRequest(BaseModel):
    name: str
    description: Optional[str] = None
