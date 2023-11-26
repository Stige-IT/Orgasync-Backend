import uuid
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, Request, status
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from app.employee.model import Employee
from app.employee.response import EmployeesCompanyResponse
from app.employee.schema import EmployeeCreateRequest
from app.users.model import UserModel
from core.database import get_db
from core.security import oauth2_scheme

employee_router = APIRouter(
    prefix="/employee",
    tags=["Employee"],
    responses={400: {"description": "Not Found"}},
    dependencies=[Depends(oauth2_scheme)]
)


# create new Employee
@employee_router.post("", status_code=status.HTTP_201_CREATED)
async def create_employee(request: Request, employee: EmployeeCreateRequest, db: Session = Depends(get_db)):
    user_registered = db.query(Employee).filter(Employee.id_user == employee.id_user).first()
    if user_registered:
        return {"message": "user already joined"}
    employee = Employee(
        id=uuid.uuid4(),
        id_user=employee.id_user,
        id_company=request.user.id,
        joined=datetime.now(),
        type=employee.type,
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


@employee_router.get("/{company_id}", status_code=status.HTTP_200_OK, response_model=Page[EmployeesCompanyResponse])
async def get_employee(company_id : str, db: Session = Depends(get_db)):
    employees = db.query(Employee).filter(Employee.id_company == company_id).all()
    return paginate(employees)


# detail employee
@employee_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=EmployeesCompanyResponse)
async def get_employee(id: str, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == id).first()
    return employee


# search employee with query in nested model Employee inside User
@employee_router.get("", status_code=status.HTTP_200_OK, response_model=Page[EmployeesCompanyResponse])
async def search_employee(query: Optional[str] = "", db: Session = Depends(get_db)):
    print(query)
    employees = db.query(Employee). \
        join(UserModel). \
        filter(UserModel.email.contains(query)). \
        all()
    return paginate(employees)


# update type employee
@employee_router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_employee(id: str, employee: EmployeeCreateRequest, db: Session = Depends(get_db)):
    result = db.query(Employee).filter(Employee.id == id).first()
    result.type = employee.type
    db.commit()
    db.refresh(employee)
    return employee


# delete employee
@employee_router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_employee(id: str, db: Session = Depends(get_db)):
    result = db.query(Employee).filter(Employee.id == id).first()
    db.delete(result)
    db.commit()
    return {"message": "deleted"}
