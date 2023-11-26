from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
from app.projects.project.model import Project
from core.database import get_db
from core.security import oauth2_scheme

project_router = APIRouter(
    prefix="/project",
    tags=["Project"],
    responses={400: {"description": "Not Found"}},
    dependencies=[Depends(oauth2_scheme)],
)


@project_router.get("", status_code=status.HTTP_200_OK)
async def get_project(id_company_project: str, db: Session = Depends(get_db)):
    projects = (
        db.query(Project).filter(Project.id_company_project == id_company_project).all()
    )
    return projects
