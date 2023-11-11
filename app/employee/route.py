from typing import Optional, List

from fastapi import APIRouter, Depends, Request, status
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from app.employee.model import Employee
from app.employee.response import EmployeesCompanyResponse
from app.users.model import UserModel
from core.database import get_db
from core.security import oauth2_scheme

employee_router = APIRouter(
    prefix="/employee",
    tags=["Employee"],
    responses={400: {"description": "Not Found"}},
    dependencies=[Depends(oauth2_scheme)]
)


@employee_router.get("", status_code=status.HTTP_200_OK, response_model=Page[EmployeesCompanyResponse])
async def get_employee(request: Request, db: Session = Depends(get_db)):
    company_id = request.user.id
    employees = db.query(Employee).filter(Employee.id_company == company_id).all()
    return paginate(employees)


# detail employee
@employee_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=EmployeesCompanyResponse)
async def get_employee(id: str, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == id).first()
    return employee


# search employee with query in nested model Employee inside User
@employee_router.post("/search/{query}", status_code=status.HTTP_200_OK, response_model=Page[EmployeesCompanyResponse])
async def search_employee(request: Request, query: Optional[str] = "", db: Session = Depends(get_db)):
    employees = db.query(Employee).\
        join(UserModel). \
        filter(UserModel.name.contains(query)). \
        filter(Employee.id_company == request.user.id). \
        all()
    return paginate(employees)
