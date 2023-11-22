from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base


class Project(Base):
    __tablename__ = "project"
    id = Column(String(100), primary_key=True, autoincrement=False)
    id_company_project = Column(String(100), ForeignKey("company_project.id"))
    company_project = relationship("CompanyProject")
    name = Column(String(100))
    description = Column(String(100))