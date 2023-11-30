from typing import Union

from pydantic import BaseModel


class LocationResponse(BaseModel):
    id: int
    name: str
    code1: Union[None, str] = None
    code2: Union[None, str] = None

    class Config:
        from_attributes = True


class AddressResponse(BaseModel):
    id: str
    street: Union[None, str] = None
    province: Union[None, LocationResponse] = None
    regency: Union[None, LocationResponse] = None
    district: Union[None, LocationResponse] = None
    village: Union[None, LocationResponse] = None
    country: Union[None, LocationResponse] = None
    zip_code: Union[None, int] = None
    lat: Union[None, str] = None
    lng: Union[None, str] = None

    class Config:
        from_attributes = True
