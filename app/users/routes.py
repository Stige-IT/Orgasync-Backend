import os
from typing import Annotated, Optional
from fastapi import (
    APIRouter,
    status,
    Depends,
    HTTPException,
    Request,
    UploadFile,
    File,
    Form,
    Query,
)
import uuid
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from core.database import get_db
from core.security import get_password_hash, oauth2_scheme, verify_password
from app.users.model import UserModel
from app.users.response import UserResponse
from app.users.schemas import CreateUserRequest, PasswordRequest, UserRequest
from app.users.services import create_user_account, update_user_account
import shutil

router = APIRouter(
    prefix="/users", tags=["Users"], responses={400: {"description": "Not Found"}}
)

user_router = APIRouter(
    prefix="/me",
    tags=["Users"],
    responses={404: {"description": "Not Found"}},
    dependencies=[Depends(oauth2_scheme)],
)


@router.get("", status_code=status.HTTP_200_OK)
async def get_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return {"data": users}


@router.get("/show/{id_user}", status_code=status.HTTP_200_OK)
async def get_detail_user(id_user: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == id_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"data": user}


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUserRequest, db: Session = Depends(get_db)):
    await create_user_account(data, db)
    payload = {"message": "User account has been succesfully created."}
    return JSONResponse(content=payload)


# search user
@router.get("/search", status_code=status.HTTP_200_OK)
async def search_user(
    query: Annotated[str, None] = None, db: Session = Depends(get_db)
):
    if query is None:
        users = db.query(UserModel).all()
        return {"data": users}
    users = (
        db.query(UserModel)
        .filter(UserModel.is_verified == True)
        .filter(UserModel.email.contains(query))
        .all()
    )
    return {"data": users}


@user_router.get("", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user_detail(request: Request, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == request.user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return request.user


@user_router.put("", status_code=status.HTTP_200_OK)
async def update_user_data(
    request: Request,
    name: Annotated[str, Form()] = None,
    email: Annotated[str, Form()] = None,
    image: Optional[UploadFile] = None,
    db: Session = Depends(get_db),
):
    user_id = request.user.id
    if image and image is not None:
        if request.user.image is not None:
            os.remove(f"uploads/{request.user.image}")
        random_string = str(uuid.uuid4())
        filename = f"{random_string}-{image.filename}"
        with open(f"uploads/{filename}", "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        await update_user_account(name, email, user_id, db, filename)
    else:
        await update_user_account(name, email, user_id, db)
    return {"message": "user profile succesfull updated"}


# edit user password
@user_router.put("/change-password", status_code=status.HTTP_200_OK)
async def update_user_password(
    request: Request,
    passwordRequest: PasswordRequest,
    db: Session = Depends(get_db),
):
    user_id = request.user.id
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(passwordRequest.password, user.password):
        raise HTTPException(status_code=401, detail="Password not match")
    user.password = get_password_hash(passwordRequest.new_password)
    db.commit()
    return {"message": "user password succesfull updated"}
