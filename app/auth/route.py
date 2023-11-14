import datetime
import random
import uuid

from fastapi import APIRouter, status, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.auth.model import CodeVerification
from app.auth.schema import LoginRequest
from app.auth.services import get_token, get_refresh_token, send_code_to_email
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


# send code for verification email
@auth_router.get("/send-code", status_code=status.HTTP_200_OK)
async def send_code(email: str, db: Session = Depends(get_db)):
    code = db.query(CodeVerification).filter(CodeVerification.email == email).first()
    expire_code = datetime.datetime.now() + datetime.timedelta(minutes=5)
    code_random = random.randint(100000, 999999)
    new_code = CodeVerification(id=uuid.uuid4(), email=email, code=code_random, expire=expire_code)
    if code:
        new_code = CodeVerification(id=uuid.uuid4(), email=email, code=code_random, expire=expire_code)
        code.code = new_code.code
        code.expire = new_code.expire
        db.commit()
    else:
        db.add(new_code)
        db.commit()
        db.refresh(new_code)
    result = await send_code_to_email(email, code_random)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
