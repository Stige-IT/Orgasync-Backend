from datetime import datetime
from typing import Union

from pydantic import BaseModel

from app.position.response import PositionResponse


class CompanyResponse(BaseModel):
    id: str
    email: Union[None, str] = None
    name: str
    code: str
    type: Union[None, str] = None
    size: Union[None, int] = None

    class Config:
        from_attributes = True


class CompanyMeResponse(BaseModel):
    id: str
    joined: Union[None, datetime] = None
    end: Union[None, datetime] = None
    type: str
    position: PositionResponse
    company: CompanyResponse

    class Config:
        from_attributes = True
