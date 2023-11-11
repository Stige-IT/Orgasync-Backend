from datetime import datetime
from typing import Union, Optional

from pydantic import BaseModel
from sqlalchemy.orm import relationship

from app.users.response import UserResponse


class EmployeesCompanyResponse(BaseModel):
    id: str
    joined: Union[None, datetime] = None
    end: Union[None, datetime] = None
    type: str
    # id_company: str
    user: Optional[UserResponse] = relationship(back_populates="employee")
