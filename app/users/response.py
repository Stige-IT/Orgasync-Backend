from datetime import datetime
from typing import Union, List

from pydantic import BaseModel, EmailStr

from app.address.response import AddressResponse


class UserResponse(BaseModel):
    id: str
    name: str
    image: Union[None, str] = None
    email: EmailStr
    is_active: bool
    is_verified: bool
    registered_at: Union[None, datetime] = None
    # id_address: str
    # address: Union[None, AddressResponse] = None

    class Config:
        from_attributes = True
