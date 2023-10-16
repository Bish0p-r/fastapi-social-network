from datetime import datetime, timedelta

from fastapi import Depends
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.dependencies import users_service
from app.users.services import UserServices
from app.utils.dependencies import ActiveAsyncSession
from app.users.repository import UserRepository
from app.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(email: str, password: str, user_services: UserServices = Depends(users_service)):
    # user = await UserRepository.find_one_or_none(email=email)
    user = await user_services.get_user_by_email(email)

    if not (user and verify_password(password, user.hashed_password)):
        return None
    return user
