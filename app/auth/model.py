from sqlalchemy import Column, String, DateTime

from core.database import Base


class CodeVerification(Base):
    __tablename__ = "code_verification"
    id = Column(String(200), primary_key=True, autoincrement=False)
    code = Column(String(200), unique=True)
    email = Column(String(200), unique=True)
    expire = Column(DateTime, nullable=True, default=None)
