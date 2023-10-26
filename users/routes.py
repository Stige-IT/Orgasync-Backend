from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from core.database import get_db
from users.schemas import CreateUserRequest
from users.services import create_user_account

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={400: {"description": "Not Found"}}
)

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not Found"}}
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUserRequest, db: Session = Depends(get_db)):
    await create_user_account(data, db)
    payload = {"message": "User account has been succesfully created."}
    return JSONResponse(content=payload)
