from fastapi import APIRouter, status, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.auth.schema import LoginRequest
from app.auth.services import get_token, get_refresh_token
from app.users.schemas import CreateUserRequest
from app.users.services import create_user_account
from core.database import get_db

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Not Found"}}
)


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: CreateUserRequest, db: Session = Depends(get_db)):
    await create_user_account(request, db)
    payload = {"message": "User account has been succesfully created."}
    return JSONResponse(content=payload, status_code=status.HTTP_201_CREATED)


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def authenticate_user(data: LoginRequest, db: Session = Depends(get_db)):
    return await get_token(data=data, db=db, is_form=False)


@auth_router.post("/token", status_code=status.HTTP_200_OK)
async def authenticate_user_from_docs(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await get_token(data=data, db=db, is_form=True)


@auth_router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_access_token(refresh_token: str = Header(), db: Session = Depends(get_db)):
    return await get_refresh_token(token=refresh_token, db=db)
