from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.projects.project.model import Project
from app.projects.project.response import ProjectResponse
from app.projects.project.schema import ProjectRequest
from core.database import get_db
from core.security import oauth2_scheme

project_router = APIRouter(
    prefix="/project",
    tags=["Project"],
    responses={400: {"description": "Not Found"}},
    dependencies=[Depends(oauth2_scheme)],
)


@project_router.get(
    "", status_code=status.HTTP_200_OK, response_model=List[ProjectResponse]
)
async def get_project(id_company_project: str, db: Session = Depends(get_db)):
    projects = (
        db.query(Project).filter(Project.id_company_project == id_company_project).all()
    )
    return projects


# create new project
@project_router.post("", status_code=status.HTTP_201_CREATED)
async def create_project(
    id_company_project: str,
    project: ProjectRequest,
    db: Session = Depends(get_db),
):
    project = Project(
        id=uuid.uuid4(),
        id_company_project=id_company_project,
        name=project.name,
        description=project.description,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return {"message": "Project has been created."}


# delete project
@project_router.delete("/{id_project}", status_code=status.HTTP_200_OK)
async def delete_project(id_project: str, db: Session = Depends(get_db)):
    exception_not_found = HTTPException(status_code=404, detail="Project not found")
    if id_project is None:
        raise exception_not_found
    project = db.query(Project).filter(Project.id == id_project).first()
    if project is None:
        raise exception_not_found
    db.delete(project)
    db.commit()
    return {"message": "Project has been deleted."}
