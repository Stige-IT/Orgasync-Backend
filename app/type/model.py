from sqlalchemy import Column, String

from core.database import Base


class TypeCompany(Base):
    __tablename__ = "type_company"
    id = Column(String(100), primary_key=True, autoincrement=False)
    name = Column(String(25))