from datetime import datetime
from typing import Union, Optional, List

from pydantic import BaseModel
from sqlalchemy.orm import relationship

from app.users.response import UserResponse


class EmployeesCompanyResponse(BaseModel):
    id: str
    joined: Union[None, datetime] = None
    end: Union[None, datetime] = None
    type: str
    # id_company: str
    user: UserResponse

    class Config:
        orm_mode = True


class ListEmployee(BaseModel):
    data: List[EmployeesCompanyResponse]

    class Config:
        orm_mode = True
