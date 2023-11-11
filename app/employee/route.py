from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.company.response import CompanyResponse
from app.employee.model import Employee
from app.employee.response import EmployeesCompanyResponse
from app.users.model import UserModel
from app.users.response import UserResponse
from core.database import get_db
from core.security import oauth2_scheme

employee_router = APIRouter(
    prefix="/employee",
    tags=["Employee"],
    responses={400: {"description": "Not Found"}},
    dependencies=[Depends(oauth2_scheme)]
)


@employee_router.get("", status_code=status.HTTP_200_OK)
async def get_employee(request: Request, db: Session = Depends(get_db)):
    company_id = request.user.id
    employees = db.query(Employee).filter(Employee.id_company == company_id).all()

    result = []
    for index, employee in enumerate(employees):
        user_data = db.query(UserModel).filter(UserModel.id == employee.id_user).first()
        employee_company = EmployeesCompanyResponse(
            id=employee.id,
            joined=employee.joined,
            end=employee.end,
            type=employee.type,
            # id_company=employee.id_company,
            user=UserResponse(
                id=user_data.id,
                name=user_data.name,
                email=user_data.email,
                is_active=user_data.is_active,
                is_verified=user_data.is_verified,
                registered_at=user_data.registered_at,
            ),
        )
        result.append(employee_company)

    return {"data": result}
