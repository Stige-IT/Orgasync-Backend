from datetime import datetime

from sqlalchemy import Column, String, DateTime, func, Integer, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base


class AddressProvince(Base):
    __tablename__ = "address_province"
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(100))


class AddressRegency(Base):
    __tablename__ = "address_regency"
    id = Column(Integer, primary_key=True, autoincrement=False)
    province_id = Column(Integer)
    name = Column(String(100))


class AddressDistrict(Base):
    __tablename__ = "address_district"
    id = Column(Integer, primary_key=True, autoincrement=False)
    regency_id = Column(Integer)
    name = Column(String(100))


class AddressVillage(Base):
    __tablename__ = "address_village"
    id = Column(Integer, primary_key=True, autoincrement=False)
    district_id = Column(Integer)
    name = Column(String(100))


class AddressCountry(Base):
    __tablename__ = "address_country"
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(100))
    code1 = Column(String(100))
    code2 = Column(String(100))


class Address(Base):
    __tablename__ = "address"
    id = Column(String(100), primary_key=True, autoincrement=False)
    street = Column(String(100))
    province_id = Column(Integer, ForeignKey("address_province.id"), nullable=True)
    province = relationship("AddressProvince", backref="address", lazy="joined")
    regency_id = Column(Integer, ForeignKey("address_regency.id"), nullable=True)
    regency = relationship("AddressRegency", backref="address", lazy="joined")
    district_id = Column(Integer, ForeignKey("address_district.id"), nullable=True)
    district = relationship("AddressDistrict", backref="address", lazy="joined")
    village_id = Column(Integer, ForeignKey("address_village.id"), nullable=True)
    village = relationship("AddressVillage", backref="address", lazy="joined")
    country_id = Column(Integer, ForeignKey("address_country.id"), nullable=True)
    country = relationship("AddressCountry", backref="address", lazy="joined")
    zip_code = Column(Integer, nullable=True)
    lat = Column(String(100), nullable=True)
    lng = Column(String(100), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
