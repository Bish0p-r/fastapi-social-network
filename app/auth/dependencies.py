from datetime import datetime
from functools import partial

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from app.users.dependencies import users_service, GetUsersService
from app.users.models import Users
from app.users.services import UserServices
from app.utils.dependencies import ActiveAsyncSession
from app.config import settings
from app.users.repository import UserRepository
from app.utils.exceptions import (
    TokenExpiredException,
    TokenAbsentException,
    IncorrectTokenException,
    UserIsNotPresentException
)


def get_token(request: Request) -> str:
    token = request.cookies.get("booking_access_token")

    if not token:
        raise TokenAbsentException

    return token


async def get_current_user(
        token: str = Depends(get_token),
        user_services: UserServices = GetUsersService
) -> Users:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise IncorrectTokenException

    expire: str = payload.get("exp")

    if not expire or int(expire) < datetime.utcnow().timestamp():
        raise TokenExpiredException

    user_id: str = payload.get("sub")

    if not user_id:
        raise UserIsNotPresentException

    user = await user_services.get_user_by_id_with_blacklist(int(user_id))
    # user = await user_services.get_user_by_id(int(user_id))

    if not user:
        raise UserIsNotPresentException

    return user


GetCurrentUser = Depends(get_current_user)

