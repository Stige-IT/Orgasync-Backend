from typing import List
import uuid
from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from sqlalchemy import asc
from sqlalchemy.orm import Session
from app.employee.model import Employee
from app.logbooks.logbook_activity.model import LogBookActivity
from app.logbooks.logbook_employee.model import LogBookEmployee
from app.logbooks.logbook_employee.response import LogBookEmployeeResponse
from app.logbooks.logbook_employee.schema import LogbookEmployeeRequest
from app.users.model import UserModel
from core.security import oauth2_scheme
from core.database import get_db


logbook_employee_router = APIRouter(
    prefix="/logbook",
    tags=["logbook"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)],
)


# get employee logbook
@logbook_employee_router.get(
    "/{id_logbook}/employee",
    status_code=200,
    response_model=Page[LogBookEmployeeResponse],
)
async def get_employee_logbook(id_logbook: str, db: Session = Depends(get_db)):
    employees = (
        db.query(LogBookEmployee)
        .join(Employee)
        .join(UserModel)
        .filter(LogBookEmployee.id_logbook == id_logbook)
        .order_by(UserModel.name.asc())
        .all()
    )
    # with total activity

    for employee in employees:
        activities = (
            db.query(LogBookActivity)
            .filter(LogBookActivity.id_logbook == id_logbook)
            .filter(LogBookActivity.id_logbook_employee == employee.id)
            .all()
        )
        # add total activity to employee
        employee.total_activity = len(activities)
    return paginate(employees)


# add employee to logbook periode
@logbook_employee_router.post("/{id_logbook}/employee", status_code=201)
async def add_employee_logbook(
    id_logbook: str, id_employees: LogbookEmployeeRequest, db: Session = Depends(get_db)
):
    for id_employee in id_employees.id_employees:
        logbook_employee = LogBookEmployee(
            id=uuid.uuid4(),
            id_logbook=id_logbook,
            id_employee=id_employee,
        )
        db.add(logbook_employee)
        db.commit()
        db.refresh(logbook_employee)

    return {"message": "success add employee to logbook"}


# remove employee from logbook periode
@logbook_employee_router.delete("/{id_logbook}/employee", status_code=200)
async def remove_employee_logbook(
    id_logbook: str, id_employees: LogbookEmployeeRequest, db: Session = Depends(get_db)
):
    if not id_employees.id_employees:
        return {"message": "employee id is empty"}
    for id_employee in id_employees.id_employees:
        logbook_employee = (
            db.query(LogBookEmployee)
            .filter(LogBookEmployee.id_logbook == id_logbook)
            .filter(LogBookEmployee.id == id_employee)
            .first()
        )
        if logbook_employee:
            db.delete(logbook_employee)
            db.commit()

    return {"message": "success remove employee from logbook"}
