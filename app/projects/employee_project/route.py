from fastapi import APIRouter, Depends, status, Request
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from app.employee.model import Employee
from app.projects.employee_project.model import EmployeeProject
from app.projects.employee_project.response import EmployeeProjectResponse
from core.database import get_db
from core.security import oauth2_scheme

employee_project_router = APIRouter(
    prefix="/employee-project",
    tags=["Project"],
    responses={400: {"description": "Not Found"}},
    dependencies=[Depends(oauth2_scheme)],
)


@employee_project_router.get(
    "", status_code=status.HTTP_200_OK, response_model=Page[EmployeeProjectResponse]
)
async def get_project(request: Request, db: Session = Depends(get_db)):
    id_user = request.user.id
    print(id_user)
    employees = db.query(Employee).filter(Employee.id_user == id_user).all()
    projects = db.query(EmployeeProject).all()
    result = []
    for employee in employees:
        for project in projects:
            if employee.id == project.id_employee:
                print(project.id_employee)
                print(project.id_project)
                result.append(project)
    return paginate(result)
