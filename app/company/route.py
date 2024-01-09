import os
import shutil
import uuid
from datetime import datetime
from typing import Annotated, List, Optional

from fastapi_pagination.utils import disable_installed_extensions_check

from fastapi import APIRouter, Form, UploadFile, status, Depends, HTTPException, Request
from fastapi_pagination import Page, paginate
from sqlalchemy import asc
from sqlalchemy.orm import Session

from app.company.model import Company
from app.company.response import CompanyDetailResponse, CompanyMeResponse, RoleResponse
from app.company.schema import CompanyRequest
from app.company.services import join_company_user
from app.employee.enums import TypeEmployeeStatus
from app.employee.model import Employee
from app.employee.response import EmployeesCompanyResponse
from app.position.constant import ownerPosition
from app.users.model import UserModel
from core.database import get_db
from core.security import get_password_hash, oauth2_scheme

disable_installed_extensions_check()

company_router = APIRouter(
    prefix="/company",
    tags=["Company"],
    responses={400: {"description": "Not Found"}},
)

company_auth_router = APIRouter(
    prefix="/company", tags=["Company"], dependencies=[Depends(oauth2_scheme)]
)


@company_router.get("", status_code=status.HTTP_200_OK)
async def get_company(db: Session = Depends(get_db)):
    company = db.query(Company).all()
    return {"data": company}


@company_auth_router.get(
    "/joined", status_code=status.HTTP_200_OK, response_model=Page[CompanyMeResponse]
)
async def get_company(request: Request, db: Session = Depends(get_db)):
    company = db.query(Employee).filter(Employee.id_user == request.user.id).all()
    return paginate(company)


# detail company
@company_auth_router.get(
    "/{id_company}",
    status_code=status.HTTP_200_OK,
    response_model=CompanyDetailResponse,
)
async def get_detail_company(id_company: str, db: Session = Depends(get_db)):
    company = db.query(Company).get(id_company)
    if not company:
        raise HTTPException(404, "Company not found")

    return company


@company_auth_router.post("", status_code=status.HTTP_201_CREATED)
async def create_company(
    request: Request, company_request: CompanyRequest, db: Session = Depends(get_db)
):
    code = uuid.uuid4()
    new_company = Company(
        id=f"com-{uuid.uuid4()}",
        id_user=request.user.id,
        name=company_request.name,
        code=str(code)[:7],
        id_type_company=company_request.type,
        size=company_request.size,
    )
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    await join_company_user(
        db, str(code)[:7], request.user.id, TypeEmployeeStatus.OWNER.value
    )
    return {"message": "company has registered"}


# update company
@company_auth_router.put("/{id_company}", status_code=status.HTTP_200_OK)
async def update_company(
    id_company: str,
    name: Annotated[str, Form()],
    image: Optional[UploadFile] = None,
    db: Session = Depends(get_db),
):
    company = db.query(Company).filter(Company.id == id_company).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with id {id_company} not found",
        )
    company.name = name
    if image and image is not None:
        if company.logo is not None:
            os.remove(f"uploads/{company.logo}")
        random_string = str(uuid.uuid4())
        filename = f"{random_string}-{image.filename}"
        company.logo = filename
        with open(f"uploads/{filename}", "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
    db.commit()
    return {"message": "company has updated"}


# delete company
@company_auth_router.delete("/{id_company}", status_code=status.HTTP_200_OK)
async def delete_company(id_company: str, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == id_company).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with id {id_company} not found",
        )
    db.delete(company)
    db.commit()
    return {"message": "company has deleted"}


@company_auth_router.post("/join", status_code=status.HTTP_201_CREATED)
async def join_company(request: Request, code: str, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.code == code).first()
    if not company:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Company not found",
                "code": "not found",
            },
        )
    id_user = request.user.id
    await join_company_user(db, code, id_user)
    return {"message": "user has joined"}


# leave company
@company_auth_router.delete("/{id_company}/leave", status_code=status.HTTP_200_OK)
async def leave_company(
    id_company: str, request: Request, db: Session = Depends(get_db)
):
    employee = (
        db.query(Employee)
        .filter(Employee.id_user == request.user.id)
        .filter(Employee.id_company == id_company)
        .first()
    )
    if not employee:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "User not found",
                "code": "not found",
            },
        )
    # check if users owner in company is only one
    owner = (
        db.query(Employee)
        .filter(Employee.id_company == id_company)
        .filter(Employee.id_position == ownerPosition)
        .count()
    )
    if owner == 1 and employee.id_position == ownerPosition:
        raise HTTPException(
            status_code=401,
            detail={
                "message": "You can't leave company, because you are the only owner",
                "code": "unauthorized",
            },
        )

    db.delete(employee)
    db.commit()
    return {"message": "user has leave"}


# add employee with email
@company_auth_router.post(
    "/{id_company}/add-employee", status_code=status.HTTP_201_CREATED
)
async def add_employee(
    id_company: str, emails: List[str], db: Session = Depends(get_db)
):
    if not emails:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Emails not found",
                "code": "not found",
            },
        )
    for email in emails:
        user = db.query(UserModel).filter(UserModel.email == email).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail={
                    "message": "User not found",
                    "code": "not found",
                },
            )
        user_registered = (
            db.query(Employee)
            .filter(Employee.id_user == user.id)
            .filter(Employee.id_company == id_company)
            .first()
        )

        if user_registered:
            raise HTTPException(401, "User has registered")
        employee = Employee(
            id=str(uuid.uuid4()),
            id_user=user.id,
            id_company=id_company,
            joined=datetime.now(),
        )
        db.add(employee)
        db.commit()
        db.refresh(employee)
    return {"message": "users has joined"}


# get employee by company id
@company_auth_router.get(
    "/{id_company}/employee",
    description="Get all employee by company id",
    status_code=status.HTTP_200_OK,
    response_model=Page[EmployeesCompanyResponse],
)
async def get_employee(id_company: str, db: Session = Depends(get_db)):
    employees = (
        db.query(Employee)
        .join(UserModel)
        .filter(Employee.id_company == id_company)
        .order_by(asc(UserModel.name))
        .all()
    )
    return paginate(employees)


# check role user in company
@company_auth_router.get(
    "/{id_company}/role", status_code=status.HTTP_200_OK, response_model=RoleResponse
)
async def check_role(request: Request, id_company: str, db: Session = Depends(get_db)):
    employee = (
        db.query(Employee)
        .filter(Employee.id_company == id_company)
        .filter(Employee.id_user == request.user.id)
        .first()
    )
    if not employee:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "User not found",
                "code": "not found",
            },
        )
    return employee
