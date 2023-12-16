from fastapi import APIRouter, Depends, status
from core.database import SessionLocal, get_db
from core.security import oauth2_scheme
from app.projects.employee_company_project.model import EmployeeCompanyProject


employee_company_project = APIRouter(
    prefix="/employee-company-project",
    tags=["Project"],
    responses={400: {"description": "Not Found"}},
    dependencies=[Depends(oauth2_scheme)],
)


@employee_company_project.get("", status_code=status.HTTP_200_OK)
async def get_employee_in_company_project(db: SessionLocal = Depends(get_db)):
    employee_project = db.query(EmployeeCompanyProject).all()
    return employee_project


@employee_company_project.post("", status_code=status.HTTP_201_CREATED)
async def add_employee_to_company_project():
    return {"message": "employee company project"}


@employee_company_project.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_employee_from_company_project(id: str):
    return {"message": "employee company project"}
