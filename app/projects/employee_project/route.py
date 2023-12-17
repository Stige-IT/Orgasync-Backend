import uuid
from fastapi import APIRouter, Depends, status, Request
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from app.employee.model import Employee
from app.projects.employee_project.model import EmployeeCompanyProject
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
    projects = db.query(EmployeeCompanyProject).all()
    result = []
    for employee in employees:
        for project in projects:
            if employee.id == project.id_employee:
                print(project.id_employee)
                print(project.id_project)
                result.append(project)
    return paginate(result)


@employee_project_router.get("/{id_employee_project}", status_code=status.HTTP_200_OK)
async def get_detail_project(id_employee_project: str, db: Session = Depends(get_db)):
    project = (
        db.query(EmployeeCompanyProject)
        .filter(EmployeeCompanyProject.id == id_employee_project)
        .first()
    )
    return project


# create employee project
@employee_project_router.post("", status_code=status.HTTP_201_CREATED)
async def create_project(
    id_employee: str,
    id_project: str,
    db: Session = Depends(get_db),
):
    project = EmployeeCompanyProject(
        id=uuid.uuid4(),
        id_employee=id_employee,
        id_project=id_project,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return {"message": "Project has been created."}


# delete employee project
@employee_project_router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_project(id: str, db: Session = Depends(get_db)):
    project = (
        db.query(EmployeeCompanyProject).filter(EmployeeCompanyProject.id == id).first()
    )
    if project:
        db.delete(project)
        db.commit()
        return {"message": "Project has been deleted."}
    return {"message": "Project not found."}
