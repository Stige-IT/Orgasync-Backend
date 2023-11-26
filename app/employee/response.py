from datetime import datetime
from typing import Union, Optional, List

from pydantic import BaseModel

from app.position.response import PositionResponse
from app.users.response import UserResponse


class TypeEmployeeResponse(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True


class EmployeesCompanyResponse(BaseModel):
    id: str
    joined: Union[None, datetime] = None
    end: Union[None, datetime] = None
    # type: str
    # company: CompanyResponse
    type: Union[None, TypeEmployeeResponse] = None
    position: Union[None, PositionResponse] = None
    user: UserResponse

    class Config:
        from_attributes = True


class ListEmployee(BaseModel):
    data: List[EmployeesCompanyResponse]

    class Config:
        from_attributes = True
