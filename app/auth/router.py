from fastapi import APIRouter, Response, status, Request
from fastapi.responses import JSONResponse

from app.auth.services import get_hash_password, verify_password, create_access_token, email_token_verification
from app.users.dependencies import GetUsersService
from app.users.services import UserServices
from app.utils.exceptions import (
    UserAlreadyExists,
    IncorrectEmailOrPassword,
    UserIsNotActiveException,
    UserIsNotPresentException,
)
from app.auth.schemas import UserRegisterSchema, UserLoginSchema, AccessToken, EmailSchema
from app.users.schemas import UserMappingSchema
from app.tasks.tasks import send_confirmation_email


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register")
async def register(request: Request, user_data: UserRegisterSchema, user_services: UserServices = GetUsersService):
    existing_user = await user_services.get_user_by_email(user_data.email)
    if existing_user:
        raise UserAlreadyExists

    hashed_password = get_hash_password(user_data.password)

    await user_services.create_user(
        email=user_data.email,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name
    )

    email_verif_token = create_access_token(data={"sub": user_data.email, "type": "email-verif"}, expire_in=60)
    verification_url = request.url_for("verify_email", token=email_verif_token)
    send_confirmation_email.delay(user_data.email, str(verification_url))
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "User created"})


@router.post("/login")
async def login(
    response: Response, user_data: UserLoginSchema, user_services: UserServices = GetUsersService
) -> AccessToken:
    user = await user_services.get_user_by_email(user_data.email)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise IncorrectEmailOrPassword
    if not user.is_active:
        raise UserIsNotActiveException

    access_token = create_access_token(data={"sub": str(user.id), "type": "access-token"})
    response.set_cookie("sn_access_token", access_token, httponly=True)
    return AccessToken(access_token=access_token)


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("sn_access_token")


@router.get("/verify-email/{token}")
async def verify_email(token: str, user_services: UserServices = GetUsersService) -> UserMappingSchema:
    return await email_token_verification(token, user_services)


@router.post("/resend-email-verification")
async def resend_email_verification(request: Request, data: EmailSchema, user_services: UserServices = GetUsersService):
    user = await user_services.get_user_by_email(data.email)
    if not user or user.is_active:
        raise UserIsNotPresentException

    email_verif_token = create_access_token(data={"sub": data.email, "type": "email-verif"}, expire_in=60)
    verification_url = request.url_for("verify_email", token=email_verif_token)
    send_confirmation_email.delay(data.email, verification_url)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Email sent"})
