from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.services import get_hash_password, verify_password, create_access_token
from app.common.dependencies import ActiveAsyncSession
from app.common.exceptions import UserAlreadyExists, IncorrectEmailOrPassword
from app.auth.schemas import UserRegisterSchema, UserLoginSchema
from app.users.repository import UserRepository


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register")
async def register(user_data: UserRegisterSchema, session: AsyncSession = ActiveAsyncSession):
    existing_user = await UserRepository.find_one_or_none(session, email=user_data.email)

    if existing_user:
        raise UserAlreadyExists

    hashed_password = get_hash_password(user_data.password)

    await UserRepository.add(
        session,
        email=user_data.email,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
    )

    return user_data


@router.post("/login")
async def login(response: Response, user_data: UserLoginSchema, session: AsyncSession = ActiveAsyncSession):
    user = await UserRepository.find_one_or_none(session, email=user_data.email)

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise IncorrectEmailOrPassword

    access_token = create_access_token(data={"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)

    return {"access_token": access_token}
