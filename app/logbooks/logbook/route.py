import uuid
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session
from app.employee.model import Employee
from app.logbooks.logbook.model import LogBook
from app.logbooks.logbook.repsonse import LogBookResponse
from app.logbooks.logbook.schema import LogBookRequest
from app.logbooks.logbook_employee.model import LogBookEmployee
from core.security import oauth2_scheme
from core.database import get_db


logbook_router = APIRouter(
    prefix="/logbook",
    tags=["logbook"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)],
)


# get logbook
@logbook_router.get("", status_code=200, response_model=Page[LogBookResponse])
async def get_logbook(request: Request, id_company: str, db: Session = Depends(get_db)):
    logbooks = db.query(LogBook).filter(LogBook.id_company == id_company).all()
    return paginate(logbooks)


# get logbook me
@logbook_router.get("/me", status_code=200, response_model=Page[LogBookResponse])
async def get_logbook_me(
    request: Request, id_company: str, db: Session = Depends(get_db)
):
    id_user = request.user.id
    id_employee = db.query(Employee).filter(Employee.id_user == id_user).first().id
    id_logbooks = (
        db.query(LogBookEmployee)
        .filter(LogBookEmployee.id_employee == id_employee)
        .all()
    )
    logbooks = []
    for id_logbook in id_logbooks:
        logbook = (
            db.query(LogBook)
            .filter(LogBook.id_company == id_company)
            .filter(LogBook.id == id_logbook.id_logbook)
            .first()
        )
        logbooks.append(logbook)

    return paginate(logbooks)


# get logbook by id
@logbook_router.get("/{id}", status_code=200, response_model=LogBookResponse)
async def get_logbook(id: str, db: Session = Depends(get_db)):
    logbook = db.query(LogBook).filter(LogBook.id == id).first()
    return logbook


# create logbook
@logbook_router.post("", status_code=201)
async def create_logbook(
    id_company: str, logbook: LogBookRequest, db: Session = Depends(get_db)
):
    logbook = LogBook(
        id=uuid.uuid4(),
        id_company=id_company,
        name=logbook.name,
        description=logbook.description,
        periode_start=logbook.periode_start,
        periode_end=logbook.periode_end,
    )
    db.add(logbook)
    db.commit()
    db.refresh(logbook)
    return logbook


# update logbook
@logbook_router.put("/{id}", status_code=200)
async def update_logbook(
    id: str, newLogBook: LogBookRequest, db: Session = Depends(get_db)
):
    logBook = db.query(LogBook).filter(LogBook.id == id).first()
    if not logBook:
        raise HTTPException(status_code=404, detail="Logbook not found")
    logBook.name = newLogBook.name
    logBook.description = newLogBook.description
    logBook.periode_start = newLogBook.periode_start
    logBook.periode_end = newLogBook.periode_end
    db.commit()
    db.refresh(logBook)
    return logBook


# delete logbook
@logbook_router.delete("/{id}", status_code=200)
async def delete_logbook(id: str, db: Session = Depends(get_db)):
    logbook = db.query(LogBook).filter(LogBook.id == id).first()
    db.delete(logbook)
    db.commit()
    return {"message": "logbook deleted"}
