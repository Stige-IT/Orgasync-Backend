from typing import List

from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session

from app.address.model import Address, AddressProvince, AddressRegency, AddressDistrict, AddressVillage, AddressCountry
from app.address.response import AddressResponse, LocationResponse
from app.address.schema import AddressRequest
from core.database import get_db
from core.security import oauth2_scheme

address_auth_router = APIRouter(
    prefix="/address/me",
    tags=["Address"],
    responses={400: {"description": "Not Found"}},
    dependencies=[Depends(oauth2_scheme)]
)

address_router = APIRouter(
    prefix="/address",
    tags=["Address"],
    responses={400: {"description": "Not Found"}},
)


@address_auth_router.get("", status_code=status.HTTP_200_OK, response_model=AddressResponse)
async def get_address(request: Request, db: Session = Depends(get_db)):
    id_address = request.user.id_address
    address = db.query(Address).get(id_address)
    return address


# update address user
@address_auth_router.put("", status_code=status.HTTP_200_OK)
async def update_address(request: Request, data: AddressRequest, db: Session = Depends(get_db)):
    id_address = request.user.id_address
    address = db.query(Address).get(id_address)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    address.street = data.street
    address.province_id = data.province
    address.regency_id = data.regency
    address.district_id = data.district
    address.village_id = data.village
    address.country_id = data.country
    address.zip_code = data.zip_code
    address.lat = data.lat
    address.lng = data.lng
    db.commit()
    return {"message": "Address has been updated"}


# get province
@address_router.get("/province", status_code=status.HTTP_200_OK, response_model=List[LocationResponse])
async def get_province(db: Session = Depends(get_db)):
    province = db.query(AddressProvince).all()
    return province


# get regency
@address_router.get("/{province_id}/regency", status_code=status.HTTP_200_OK, response_model=List[LocationResponse])
async def get_regency(province_id: int, db: Session = Depends(get_db)):
    regency = db.query(AddressRegency).filter(AddressRegency.province_id == province_id).all()
    return regency


# get district
@address_router.get("/{regency_id}/district", status_code=status.HTTP_200_OK, response_model=List[LocationResponse])
async def get_district(regency_id: int, db: Session = Depends(get_db)):
    district = db.query(AddressDistrict).filter(AddressDistrict.regency_id == regency_id).all()
    return district


# get village
@address_router.get("/{district_id}/village", status_code=status.HTTP_200_OK, response_model=List[LocationResponse])
async def get_village(district_id: int, db: Session = Depends(get_db)):
    village = db.query(AddressVillage).filter(AddressVillage.district_id == district_id).all()
    return village


# get country
@address_router.get("/country", status_code=status.HTTP_200_OK, response_model=List[LocationResponse])
async def get_country(db: Session = Depends(get_db)):
    country = db.query(AddressCountry).all()
    return country
