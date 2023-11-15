from datetime import datetime
from typing import Union, Optional, List

from pydantic import BaseModel
from sqlalchemy.orm import relationship

from app.company.response import CompanyResponse
from app.position.response import PositionResponse
from app.users.response import UserResponse


class EmployeesCompanyResponse(BaseModel):
    id: str
    joined: Union[None, datetime] = None
    end: Union[None, datetime] = None
    type: str
    # company: CompanyResponse
    position: Union[None, PositionResponse] = None
    user: UserResponse

    class Config:
        from_attributes = True


class ListEmployee(BaseModel):
    data: List[EmployeesCompanyResponse]

    class Config:
        from_attributes = True
