from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.config import settings
from app.auth.services import authenticate_user, create_access_token
from app.auth.dependencies import get_current_user
from app.users.dependencies import GetUsersService
from app.users.repository import UserRepository
from app.users.services import UserServices


class AdminAuth(AuthenticationBackend):
    async def login(
            self,
            request: Request,
            user_services=UserServices(UserRepository)
    ) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        user = await authenticate_user(email, password, user_services)
        if user and user.is_superuser:
            access_token = create_access_token({"sub": str(user.id)})
            request.session.update({"token": access_token})
            return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(
            self,
            request: Request,
            user_services=UserServices(UserRepository)
    ) -> bool:
        token = request.session.get("token")
        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        user = await get_current_user(token, user_services)
        if not user:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        return True


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
