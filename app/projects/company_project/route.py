import shutil
from typing import Annotated, Optional
import uuid
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, status, Request
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from app.projects.company_project.model import CompanyProject
from app.projects.company_project.response import (
    CompanyProjectResponse,
    CompanyProjectResult,
)
from app.projects.company_project.schema import (
    CompanyProjectRequest,
    EmployeeProjectRequest,
)
from app.projects.employee_project.model import EmployeeCompanyProject
from app.projects.project.model import Project
from core.database import get_db
from core.security import oauth2_scheme

company_project_router = APIRouter(
    prefix="/company/project", tags=["Project"], dependencies=[Depends(oauth2_scheme)]
)


@company_project_router.get(
    "", status_code=status.HTTP_200_OK, response_model=Page[CompanyProjectResponse]
)
async def get_project(id_company: str, db: Session = Depends(get_db)):
    projects = (
        db.query(CompanyProject).filter(CompanyProject.id_company == id_company).all()
    )

    return paginate(projects)


# create company project
@company_project_router.post("", status_code=status.HTTP_201_CREATED)
async def create_project(
    id_company: str,
    name: Annotated[str, Form()],
    description: Annotated[str, Form()] = None,
    image: Optional[UploadFile] = None,
    db: Session = Depends(get_db),
):
    project = CompanyProject(
        id=uuid.uuid4(),
        id_company=id_company,
        name=name,
        description=description,
    )
    if image:
        project.image = image.filename
        with open(f"uploads/{image.filename}", "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
    db.add(project)
    db.commit()
    db.refresh(project)
    return {"message": "Project has been created."}


# detail company project
@company_project_router.get(
    "/{id}", status_code=status.HTTP_200_OK, response_model=CompanyProjectResult
)
async def detail_project(id: str, db: Session = Depends(get_db)):
    company_project = db.query(CompanyProject).filter(CompanyProject.id == id).first()
    if company_project:
        employee = (
            db.query(EmployeeCompanyProject)
            .filter(EmployeeCompanyProject.id_project == id)
            .all()
        )
        print(company_project.id)
        projects = (
            db.query(Project)
            .filter(Project.id_company_project == company_project.id)
            .all()
        )
        if not company_project:
            company_project = []
        return CompanyProjectResult(
            company_project=company_project,
            total_employee=len(employee),
            employee=employee,
            total_project=len(projects),
            project=projects,
        )
    return HTTPException(status_code=404, detail="Project not found.")


# delete company project
@company_project_router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_project(id: str, db: Session = Depends(get_db)):
    project = db.query(CompanyProject).filter(CompanyProject.id == id).first()
    if project:
        db.delete(project)
        db.commit()
        return {"message": "Project has been deleted."}
    return {"message": "Project not found."}


# add employee to company project
@company_project_router.post("/add-employee", status_code=status.HTTP_201_CREATED)
async def add_employee_to_project(
    project_id: str,
    employessRequest: EmployeeProjectRequest,
    db: Session = Depends(get_db),
):
    for id_employee in employessRequest.employee_id:
        employee_project = EmployeeCompanyProject(
            id=uuid.uuid4(),
            id_employee=id_employee,
            id_project=project_id,
        )
        db.add(employee_project)
        db.commit()
        db.refresh(employee_project)
    return {"message": "Employee has been added to project."}
