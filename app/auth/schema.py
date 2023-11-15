from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class VerificationRequest(BaseModel):
    email: EmailStr
    code: int
