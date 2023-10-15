from fastapi import HTTPException, status


class AuthException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExists(AuthException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "User with this email already exists"


class IncorrectEmailOrPassword(AuthException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Incorrect email or password"
