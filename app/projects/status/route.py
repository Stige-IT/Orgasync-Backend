from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.projects.status.model import Status
from core.database import get_db
from core.security import oauth2_scheme


status_router = APIRouter(
    prefix="/status",
    tags=["Task"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)],
)


# get status
@status_router.get("")
async def get_status(db: Session = Depends(get_db)):
    status = db.query(Status).order_by(Status.level.desc()).order_by(Status.name).all()
    return status
