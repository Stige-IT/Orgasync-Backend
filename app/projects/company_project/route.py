import os
import shutil
from typing import Annotated, Optional
import uuid
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, status, Request
from fastapi_pagination import Page, paginate
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.projects.company_project.model import CompanyProject
from app.projects.company_project.response import (
    CompanyProjectResponse,
    CompanyProjectResult,
)
from app.projects.company_project.schema import CompanyProjectRequest
from app.projects.employee_company_project.model import EmployeeCompanyProject
from app.projects.project.model import Project
from core.database import get_db
from core.security import oauth2_scheme

company_project_router = APIRouter(
    prefix="/company-project",
    tags=["Company Project"],
    dependencies=[Depends(oauth2_scheme)],
)


@company_project_router.get(
    "", status_code=status.HTTP_200_OK, response_model=Page[CompanyProjectResponse]
)
async def get_project(id_company: str, db: Session = Depends(get_db)):
    projects = (
        db.query(CompanyProject)
        .filter(CompanyProject.id_company == id_company)
        .order_by(desc(CompanyProject.created_at))
        .all()
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
            .filter(EmployeeCompanyProject.id_company_project == id)
            .all()
        )
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
            # employee=employee,
            total_project=len(projects),
            # project=projects,
        )
    return HTTPException(status_code=404, detail="Project not found.")


# update company project
@company_project_router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_project(
    id: str,
    name: Annotated[str, Form()],
    description: Annotated[str, Form()] = None,
    image: Optional[UploadFile] = None,
    db: Session = Depends(get_db),
):
    company_project = db.query(CompanyProject).filter(CompanyProject.id == id).first()
    if company_project:
        if image:
            # remove old image
            if company_project.image is not None:
                os.remove(f"uploads/{company_project.image}")
            company_project.image = image.filename
            with open(f"uploads/{image.filename}", "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
        company_project.name = name
        company_project.description = description
        db.commit()
        db.refresh(company_project)
        return {"message": "Project has been updated."}
    raise HTTPException(status_code=404, detail="Project not found.")


# delete company project
@company_project_router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_project(id: str, db: Session = Depends(get_db)):
    project = db.query(CompanyProject).filter(CompanyProject.id == id).first()
    if project:
        db.delete(project)
        db.commit()
        return {"message": "Project has been deleted."}
    return {"message": "Project not found."}
