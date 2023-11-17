from sqlalchemy import Column, String, ForeignKey

from core.database import Base


class CompanyProject(Base):
    __tablename__ = "company_project"
    id = Column(String(100), primary_key=True, autoincrement=False)
    id_company = Column(String(100), ForeignKey("company.id"))
    name = Column(String(100))

