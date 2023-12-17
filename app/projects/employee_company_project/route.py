from fastapi import APIRouter, Depends, status
from app.projects.company_project.model import CompanyProject
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
    employee_project = (
        db.query(EmployeeCompanyProject)
        .join(CompanyProject)
        .filter(CompanyProject.id == EmployeeCompanyProject.id_company_project)
        .all()
    )
    return employee_project
