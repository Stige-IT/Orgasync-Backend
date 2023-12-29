from sqlalchemy import Column, DateTime, String, ForeignKey, Text, func
from sqlalchemy.orm import relationship

from core.database import Base


class CompanyProject(Base):
    __tablename__ = "company_project"
    id = Column(String(100), primary_key=True, autoincrement=False)
    id_company = Column(String(100), ForeignKey("company.id", ondelete="CASCADE"))
    company = relationship("Company", backref="company_project", lazy="joined")
    name = Column(String(100))
    description = Column(String(255), nullable=True)
    image = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
