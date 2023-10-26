from datetime import datetime

from fastapi import HTTPException

from core.security import get_password_hash
from users.model import UserModel


async def create_user_account(data, db):
    user = db.query(UserModel).filter(UserModel.email == data.email).first()
    if user:
        raise HTTPException(status_code=422, detail="Email is already registered with us")

    new_user = UserModel(
        name=data.name,
        email=data.email,
        password=get_password_hash(data.password),
        is_active=False,
        is_verified=False,
        registered_at=datetime.now(),
        updated_at=datetime.now()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
