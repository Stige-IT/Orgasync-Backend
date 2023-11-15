import uuid
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.security import get_password_hash
from app.users.model import UserModel


async def create_user_account(data, db):
    user = db.query(UserModel).filter(UserModel.email == data.email).first()
    if user:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Email is already registered with us",
                "email": "registered",
            },
        )

    new_user = UserModel(
        id=f"usr-{uuid.uuid4()}",
        name=data.name,
        email=data.email,
        password=get_password_hash(data.password),
        is_active=True,
        is_verified=False,
        registered_at=datetime.now(),
        updated_at=datetime.now(),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_user_account(name, email, id_user, image, db: Session):
    user = db.query(UserModel).filter(UserModel.id == id_user).first()
    if not user:
        raise HTTPException(
            status_code=422, detail="Email is not already registered with us"
        )
    user.name = name
    user.email = email
    user.image = image
    db.commit()
    return True
