from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.projects.priotity.model import Priority
from core.database import get_db
from core.security import oauth2_scheme


priority_router = APIRouter(
    prefix="/priority",
    tags=["priority"],
    dependencies=[Depends(oauth2_scheme)],
)


# get all priority
@priority_router.get("")
async def get_priority(db: Session = Depends(get_db)):
    priorities = db.query(Priority).all()
    return priorities
