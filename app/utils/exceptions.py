from fastapi import HTTPException, status


class AuthException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExists(AuthException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "User with this email already exists"


class UserIsNotPresentException(AuthException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "User is not present"


class IncorrectEmailOrPassword(AuthException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Incorrect email or password"


class TokenExpiredException(AuthException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token expired"


class IncorrectTokenException(AuthException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect token"


class TokenAbsentException(AuthException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token absent"
