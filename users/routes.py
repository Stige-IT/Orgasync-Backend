from fastapi import APIRouter, status, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from core.database import get_db
from core.security import oauth2_scheme
from users.model import UserModel
from users.response import UserResponse
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
    responses={404: {"description": "Not Found"}},
    dependencies=[Depends(oauth2_scheme)]
)


@router.get("", status_code=status.HTTP_200_OK)
async def get_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return {"data": users}


@router.get("/{id_user}", status_code=status.HTTP_200_OK)
async def get_detail_user(id_user: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == id_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"data": user}


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUserRequest, db: Session = Depends(get_db)):
    await create_user_account(data, db)
    payload = {"message": "User account has been succesfully created."}
    return JSONResponse(content=payload)


@user_router.post('/me', status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user_detail(request: Request):
    return request.user
