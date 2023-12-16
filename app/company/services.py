import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.company.model import Company
from app.employee.model import Employee


async def join_company_user(db: Session, code: str, id_user: str, type_employee=None):
    user_registered = db.query(Employee).filter(Employee.id_user == id_user).first()
    company_registered = db.query(Company).filter(Company.code == code).first()
    if not company_registered:
        raise HTTPException(status_code=404, detail="company not found")
    if user_registered and company_registered.id == user_registered.id_company:
        raise HTTPException(status_code=400, detail="user already joined")
    new_employee = Employee(
        id=str(uuid.uuid4()),
        id_user=id_user,
        id_company=company_registered.id,
    )
    if type_employee:
        new_employee.id_type = type_employee
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return True
