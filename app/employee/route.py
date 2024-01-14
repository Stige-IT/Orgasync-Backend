import uuid
from datetime import datetime
from typing import Annotated, Optional, List

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi_pagination import Page, paginate
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.employee.model import Employee, TypeEmployee
from app.employee.response import EmployeesCompanyResponse
from app.employee.schema import EmployeeCreateRequest
from app.users.model import UserModel
from core.database import get_db
from core.security import oauth2_scheme

employee_router = APIRouter(
    prefix="/employee",
    tags=["Employee"],
    responses={400: {"description": "Not Found"}},
    dependencies=[Depends(oauth2_scheme)],
)


@employee_router.get(
    "/{company_id}",
    status_code=status.HTTP_200_OK,
    response_model=Page[EmployeesCompanyResponse],
)
async def get_employee(company_id: str, db: Session = Depends(get_db)):
    employees = db.query(Employee).filter(Employee.id_company == company_id).all()
    return paginate(employees)


# detail employee
@employee_router.get(
    "/{id}", status_code=status.HTTP_200_OK, response_model=EmployeesCompanyResponse
)
async def get_employee(id: str, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == id).first()
    return employee


# search employee with query in nested model Employee inside User
@employee_router.get(
    "/search/{id_company}",
    status_code=status.HTTP_200_OK,
    response_model=Page[EmployeesCompanyResponse],
)
async def search_employee(
    id_company: str,
    query: Optional[str] = "",
    db: Session = Depends(get_db),
):
    employees = (
        db.query(Employee)
        .join(UserModel)
        .filter(Employee.id_company == id_company)
        .filter((UserModel.email.contains(query)) | (UserModel.name.contains(query)))
        .all()
    )
    for employee in employees:
        print(employee.user.email)
    return paginate(employees)


# update type employee
@employee_router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_employee(
    id: str,
    id_type_employee: Annotated[str, Form()] = None,
    db: Session = Depends(get_db),
):
    result = db.query(Employee).filter(Employee.id == id).first()
    result.id_type = id_type_employee
    db.commit()
    return {
        "message": "updated",
        "data": {"id": result.id, "id_type_employee": result.id_type},
    }


# delete employee
@employee_router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_employee(id: str, db: Session = Depends(get_db)):
    result = db.query(Employee).filter(Employee.id == id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(result)
    db.commit()
    return {"message": "deleted"}


# Type Employee
# get type employee
@employee_router.get("/show/type", status_code=status.HTTP_200_OK)
async def get_type_employee(db: Session = Depends(get_db)):
    employees = db.query(TypeEmployee).order_by(TypeEmployee.name).all()
    return employees


# create type employee
@employee_router.post("/create/type", status_code=status.HTTP_201_CREATED)
async def create_type_employee(name: str, level: int, db: Session = Depends(get_db)):
    type_employee = TypeEmployee(id=uuid.uuid4(), name=name, level=level)
    db.add(type_employee)
    db.commit()
    db.refresh(type_employee)
    return type_employee
