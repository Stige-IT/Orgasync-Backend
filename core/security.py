from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from core.config import get_settings

settings = get_settings()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_password_hash(password):
    return pwd_context.hash(password)
