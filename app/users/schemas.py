from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserRequest(BaseModel):
    name: str
    email: EmailStr
