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


class UserIsNotActiveException(AuthException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "User is not active"


class FriendShipException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class FriendShipAlreadyExists(FriendShipException):
    detail = "Friendship already exists"


class FriendShipRequestAlreadyExists(FriendShipException):
    detail = "Friendship request already exists"


class FriendShipCannotBeSentToYourself(FriendShipException):
    detail = "Friendship cannot be sent to yourself"


class IncorrectUserIdException(FriendShipException):
    detail = "User with this id does not exist"


class BlackListException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyInBlackListException(BlackListException):
    detail = "User is already in blacklist"


class PostsException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class YouAreNotPostAuthorOrIncorrectPostIDException(PostsException):
    detail = "You are not post author or incorrect post ID"


class IncorrectPostIdException(PostsException):
    detail = "Incorrect post ID"


class LikesException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class YouHaveAlreadyLikedThisPostException(LikesException):
    detail = "You have already liked this post"



