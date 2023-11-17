from fastapi import APIRouter, Depends, status, Request
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from app.projects.company_project.model import CompanyProject
from app.projects.company_project.response import CompanyProjectResponse
from core.database import get_db
from core.security import oauth2_scheme

company_project_router = APIRouter(
    prefix="/company/project",
    tags=["Project"],
    dependencies=[Depends(oauth2_scheme)]
)


@company_project_router.get("", status_code=status.HTTP_200_OK, response_model=Page[CompanyProjectResponse])
async def get_project(request: Request, db: Session = Depends(get_db)):
    company_project = db.query(CompanyProject).filter(CompanyProject.id_company == request.user.id).all()
    return paginate(company_project)
