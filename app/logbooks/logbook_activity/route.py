import shutil
from typing import Annotated, List, Optional
import uuid
from fastapi import APIRouter, Depends, Form, Request, UploadFile
from sqlalchemy.orm import Session
from app.employee.model import Employee
from app.logbooks.logbook_activity.model import LogBookActivity
from app.logbooks.logbook_employee.model import LogBookEmployee
from core.security import oauth2_scheme
from core.database import get_db


logbook_activity_router = APIRouter(
    prefix="/logbook",
    tags=["logbook"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)],
)


# get logbook activities
@logbook_activity_router.get("/employee/{id_employee}/activity", status_code=200)
async def get_logbook_activity(id_employee: str, db: Session = Depends(get_db)):
    activities = (
        db.query(LogBookActivity)
        .filter(LogBookActivity.id_logbook_employee == id_employee)
        .order_by(LogBookActivity.created_at.asc())
        .all()
    )
    # create output logbook grouping by month in format datetime
    # output is array
    output = []
    for activity in activities:
        # datetime format to example : 01-01-2021
        month = activity.created_at.strftime("%B")
        # check if month is already in output
        # if month is already in output, append activity to month
        # else create new month and append activity to month
        if any(month in d["month"] for d in output):
            for d in output:
                if d["month"] == month:
                    d["activities"].append(activity)
        else:
            output.append({"month": month, "activities": [activity]})

    return output


# get logbook activities me
@logbook_activity_router.get("/activity/me", status_code=200)
async def get_logbook_activity_me(
    request: Request, id_logbook: str, db: Session = Depends(get_db)
):
    id_user = request.user.id
    id_employee = (
        db.query(LogBookEmployee)
        .join(Employee)
        .filter(Employee.id_user == id_user)
        .first()
        .id
    )

    activities = (
        db.query(LogBookActivity)
        .filter(LogBookActivity.id_logbook_employee == id_employee)
        .filter(LogBookActivity.id_logbook == id_logbook)
        .order_by(LogBookActivity.created_at.asc())
        .all()
    )
    # create output logbook grouping by month in format datetime
    # output is array
    output = []
    for activity in activities:
        # datetime format to example : 01-01-2021
        month = activity.created_at.strftime("%B")
        # check if month is already in output
        # if month is already in output, append activity to month
        # else create new month and append activity to month
        if any(month in d["month"] for d in output):
            for d in output:
                if d["month"] == month:
                    d["activities"].append(activity)
        else:
            output.append({"month": month, "activities": [activity]})

    return output


# add logbook activity
@logbook_activity_router.post("/employee/activity/me", status_code=201)
async def add_logbook_activity(
    request: Request,
    id_logbook: Annotated[str, Form()],
    description: Annotated[str, Form()],
    rating: Annotated[int, Form()],
    image: Optional[UploadFile] = None,
    db: Session = Depends(get_db),
):
    id_user = request.user.id
    id_employee = (
        db.query(LogBookEmployee)
        .join(Employee)
        .filter(Employee.id_user == id_user)
        .first()
        .id
    )
    logbook_activity = LogBookActivity(
        id=uuid.uuid4(),
        id_logbook=id_logbook,
        id_logbook_employee=id_employee,
        description=description,
        rating=rating,
    )
    if image and image is not None:
        random_string = str(uuid.uuid4())
        filename = f"{random_string}-{image.filename}"
        logbook_activity.image = filename
        with open(f"uploads/{filename}", "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
    db.add(logbook_activity)
    db.commit()
    db.refresh(logbook_activity)
    return logbook_activity


# delete logbook activity
@logbook_activity_router.delete("/employee/activity/{id}", status_code=200)
async def remove_logbok_activity(id: str, db: Session = Depends(get_db)):
    logbook_activity = (
        db.query(LogBookActivity).filter(LogBookActivity.id == id).first()
    )
    db.delete(logbook_activity)
    db.commit()
    return {"message": "success delete logbook activity"}
