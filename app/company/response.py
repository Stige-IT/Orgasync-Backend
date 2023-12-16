from datetime import datetime
from typing import Union

from pydantic import BaseModel, EmailStr

from app.address.response import AddressResponse
from app.employee.response import TypeEmployeeResponse
from app.position.response import PositionResponse
from app.type.response import TypeResponse
from app.users.response import UserResponse


class CompanyResponse(BaseModel):
    id: str
    name: str
    description: Union[None, str] = None
    logo: Union[None, str] = None
    cover: Union[None, str] = None
    code: str
    size: Union[None, int] = None
    owner: UserResponse
    type_company: TypeResponse
    address: Union[None, AddressResponse] = None

    class Config:
        from_attributes = True


class CompanyMeResponse(BaseModel):
    id: str
    joined: Union[None, datetime] = None
    end: Union[None, datetime] = None
    position: Union[None, PositionResponse] = None
    company: CompanyResponse
    type: Union[None, TypeEmployeeResponse] = None

    class Config:
        from_attributes = True


class OwnerResponse(BaseModel):
    id: str
    name: str
    image: Union[None, str] = None
    email: EmailStr

    class Config:
        from_attributes = True


class CompanyDetailResponse(BaseModel):
    id: str
    name: str
    description: Union[None, str] = None
    logo: Union[None, str] = None
    cover: Union[None, str] = None
    code: str
    size: Union[None, int] = None
    owner: OwnerResponse
    type_company: TypeResponse
    address: Union[None, AddressResponse] = None

    class Config:
        from_attributes = True


class RoleResponse(BaseModel):
    type: Union[None, TypeEmployeeResponse] = None

    class Config:
        from_attributes = True
