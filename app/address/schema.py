from pydantic import BaseModel


class AddressRequest(BaseModel):
    street: str
    province: int
    regency: int
    district: int
    village: int
    country: int
    zip_code: int
    lat: str
    lng: str
