from datetime import timedelta

from fastapi import HTTPException
from fastapi_mail import MessageSchema, FastMail
from sqlalchemy.orm import Session

from app.auth.response import TokenResponse
from app.auth.template import template_body
from app.company.model import Company
from core.config import get_settings, configMail
from core.security import verify_password, get_token_payload, create_access_token, create_refresh_token
from app.users.model import UserModel

settings = get_settings()


async def get_token(data, db: Session, is_form: bool):
    if is_form:
        user: UserModel = db.query(UserModel).filter(UserModel.email == data.username).first()
        if not user:
            user: Company = db.query(Company).filter(Company.email == data.username).first()
    else:
        user: UserModel = db.query(UserModel).filter(UserModel.email == data.email).first()
        if not user:
            user: Company = db.query(Company).filter(Company.email == data.email).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Email is not registered with us.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid Login Credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    _verify_user_access(user)
    return await _get_user_token(user)


def _verify_user_access(user):
    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Your account is not active. Please contact support.",
                "email": "not_active",
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_verified:
        # Trigger user account verification email
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Your account is not verified. Please verify your account.",
                "email": "not_verified",
            },
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_refresh_token(token, db):
    payload = get_token_payload(token=token)
    user_id = payload.get('id', None)
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await _get_user_token(user=user, refresh_token=token)


async def _get_user_token(user, refresh_token=None):
    payload = {"id": user.id}

    access_token_expiry = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = await create_access_token(payload, access_token_expiry)
    if not refresh_token:
        refresh_token = await create_refresh_token(payload)
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=access_token_expiry.seconds  # in seconds
    )


async def send_code_to_email(email: str, code: int):
    try:
        message = MessageSchema(
            subject="Verification Code for Email",
            recipients=[email],  # List of recipients, as many as you can pass
            body=template_body(code),
            subtype="html"
        )

        fm = FastMail(configMail)
        await fm.send_message(message)
        return True
    except Exception as e:
        print(e)
        return False
