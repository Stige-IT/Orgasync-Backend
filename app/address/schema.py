from typing import Union
from pydantic import BaseModel


class AddressRequest(BaseModel):
    street: Union[None, str] = None
    province: Union[None, int] = None
    regency: Union[None, int] = None
    district: Union[None, int] = None
    village: Union[None, int] = None
    country: Union[None, int] = None
    zip_code: Union[None, int] = None
    # lat and lng is optional
    lat: Union[None, str] = None
    lng: Union[None, str] = None
