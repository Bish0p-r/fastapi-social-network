from datetime import datetime, timedelta

from fastapi import Depends
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.dependencies import GetUsersService, GetProfileService
from app.users.services import UserServices, UserProfileService
from app.utils.dependencies import ActiveAsyncSession
from app.users.repository import UserRepository
from app.config import settings
from app.utils.exceptions import IncorrectTokenException, TokenExpiredException, UserIsNotPresentException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expire_in: int = 15) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expire_in)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(
        email: str,
        password: str,
        user_services: UserServices = GetUsersService,
):
    user = await user_services.get_user_by_email(email)

    if not (user and verify_password(password, user.hashed_password)):
        return None
    return user


async def email_token_verification(
        token: str,
        user_services: UserServices = GetUsersService,
        profile_services: UserProfileService = GetProfileService
):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise IncorrectTokenException

    expire: str = payload.get("exp")

    if not expire or int(expire) < datetime.utcnow().timestamp():
        raise TokenExpiredException

    user_email: str = payload.get("sub")
    token_type: str = payload.get("type")

    if not token_type or not user_email or token_type != "email-verif":
        raise IncorrectTokenException

    user = await user_services.activate_user(user_email)
    user_id = user.Users.id

    if not user_id:
        raise UserIsNotPresentException

    await profile_services.create_user_profile(user_id)

    return user
