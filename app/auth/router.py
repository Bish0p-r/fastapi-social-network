from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.services import get_hash_password, verify_password, create_access_token, email_token_verification
from app.users.dependencies import users_service, GetUsersService
from app.users.services import UserServices
from app.utils.dependencies import ActiveAsyncSession
from app.utils.exceptions import UserAlreadyExists, IncorrectEmailOrPassword, UserIsNotActiveException
from app.auth.schemas import UserRegisterSchema, UserLoginSchema, AccessToken
from app.users.repository import UserRepository


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register")
async def register(user_data: UserRegisterSchema, user_services: UserServices = Depends(users_service)):
    existing_user = await user_services.get_user_by_email(user_data.email)

    if existing_user:
        raise UserAlreadyExists

    hashed_password = get_hash_password(user_data.password)

    await user_services.create_user(
        email=user_data.email,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
    )

    email_verif_token = create_access_token(data={"sub": user_data.email, "type": "email-verif"}, expire_in=60)

    print(email_verif_token)

    return Response(status_code=status.HTTP_201_CREATED, content="User created")


@router.post("/login")
async def login(
        response: Response,
        user_data: UserLoginSchema,
        user_services: UserServices = Depends(users_service)
) -> AccessToken:
    user = await user_services.get_user_by_email(user_data.email)

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise IncorrectEmailOrPassword

    # if not user.is_active:
    #     raise UserIsNotActiveException

    access_token = create_access_token(data={"sub": str(user.id), "type": "access-token"})
    response.set_cookie("booking_access_token", access_token, httponly=True)

    return AccessToken(access_token=access_token)


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("booking_access_token")


@router.get("/verify-email/{token}")
async def verify_email(token: str, user_services: UserServices = GetUsersService):
    return await email_token_verification(token, user_services)
