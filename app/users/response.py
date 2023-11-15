from datetime import datetime
from typing import Union, List

from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: str
    name: str
    image: Union[None, str] = None
    email: EmailStr
    is_active: bool
    is_verified: bool
    registered_at: Union[None, datetime] = None

    class Config:
        from_attributes = True
