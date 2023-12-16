from fastapi import APIRouter, Depends
from app.position.model import Position

from core.database import SessionLocal, get_db


position_router = APIRouter(
    prefix="/position",
    tags=["Position"],
    responses={400: {"description": "Not Found"}},
)


@position_router.get("")
async def get_position(db: SessionLocal = Depends(get_db)):
    positions = db.query(Position).all()
    return {"data": positions}
