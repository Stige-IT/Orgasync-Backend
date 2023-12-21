import uuid
from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page, paginate
from app.projects.company_project.model import CompanyProject
from app.projects.employee_company_project.response import (
    EmployeeCompanyProjectResponse,
)
from app.projects.employee_company_project.schema import EmployeeProjectRequest
from core.database import get_db
from core.security import oauth2_scheme
from sqlalchemy.orm import Session
from app.projects.employee_company_project.model import EmployeeCompanyProject


employee_company_project = APIRouter(
    prefix="/company-project",
    tags=["Company Project"],
    responses={400: {"description": "Not Found"}},
    dependencies=[Depends(oauth2_scheme)],
)


@employee_company_project.get(
    "/{id_company_project}/employee",
    status_code=status.HTTP_200_OK,
    response_model=Page[EmployeeCompanyProjectResponse],
)
async def get_employee_in_company_project(
    id_company_project: str, db: Session = Depends(get_db)
):
    employee_project = (
        db.query(EmployeeCompanyProject)
        .join(CompanyProject)
        .filter(CompanyProject.id == id_company_project)
        .all()
    )
    return paginate(employee_project)


# add employee to company project
@employee_company_project.post(
    "{company_project_id}/employee/add", status_code=status.HTTP_201_CREATED
)
async def add_employee_to_project(
    company_project_id: str,
    employessRequest: EmployeeProjectRequest,
    db: Session = Depends(get_db),
):
    for id_employee in employessRequest.employee_id:
        employee_project = EmployeeCompanyProject(
            id=uuid.uuid4(),
            id_employee=id_employee,
            id_company_project=company_project_id,
        )
        db.add(employee_project)
        db.commit()
        db.refresh(employee_project)
    return {"message": "Employee has been added to project."}
