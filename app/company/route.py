import uuid

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.auth.schema import LoginRequest
from app.auth.services import get_token
from app.company.model import Company
from app.company.schema import CompanyRequest
from app.employee.model import Employee
from core.database import get_db
from core.security import get_password_hash

company_router = APIRouter(
    prefix="/company",
    tags=["Company"],
    responses={400: {"description": "Not Found"}}
)


@company_router.post("/login", status_code=status.HTTP_200_OK)
async def login_company(request: LoginRequest, db: Session = Depends(get_db)):
    return await get_token(data=request, db=db, is_form=False)


@company_router.get("", status_code=status.HTTP_200_OK)
async def get_company(db: Session = Depends(get_db)):
    company = db.query(Company).all()
    return {"data": company}


@company_router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_company(request: CompanyRequest, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.email == request.email).first()
    if company:
        raise HTTPException(status_code=422,
                            detail={"message": "Email is already registered with us", "email": "registered"}
                            )

    code = uuid.uuid4()
    new_company = Company(
        id=uuid.uuid4(),
        name=request.name,
        email=request.email,
        password=get_password_hash(request.password),
        code=str(code)[:7],
        type=request.type,
        size=request.size,
    )
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company


# check name if exist
@company_router.get("/check-name/{name}", status_code=status.HTTP_200_OK)
async def check_name(name: str, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.name == name).first()
    if company:
        raise HTTPException(status_code=422,
                            detail={"message": "Name is already registered with us", "name": "registered"}
                            )
    return JSONResponse(content={"message": "Name is available"}, status_code=status.HTTP_200_OK)


@company_router.post("/join", status_code=status.HTTP_201_CREATED)
async def join_company(id_user: str, code: str, db: Session = Depends(get_db)):
    user_registered = db.query(Employee).filter(Employee.id_user == id_user).first()
    if user_registered:
        return {"message": "user already joined"}
    company = db.query(Company).filter(Company.code == code).first()
    new_employee = Employee(
        id=uuid.uuid4(),
        id_user=id_user,
        id_company=company.id,
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee
