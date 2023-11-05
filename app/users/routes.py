from typing import Annotated, Optional
from fastapi import APIRouter, status, Depends, HTTPException, Request, UploadFile, File, Form
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from core.database import get_db
from core.security import oauth2_scheme
from app.users.model import UserModel
from app.users.response import UserResponse
from app.users.schemas import CreateUserRequest, UserRequest
from app.users.services import create_user_account, update_user_account

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={400: {"description": "Not Found"}}
)

user_router = APIRouter(
    prefix="/me",
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


@user_router.get('', status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user_detail(request: Request):
    return request.user


@user_router.put('', status_code=status.HTTP_200_OK)
async def update_user_data(
        request: Request,
        name: Annotated[str, Form()],
        email: Annotated[str, Form()],
        image: Optional[UploadFile] = None,
        db: Session = Depends(get_db),
):
    user_id = request.user.id
    result = await update_user_account(name, email, user_id, image.filename, db)
    return {
        "status": result,
        "message": "user profile succesfull updated"
    }
