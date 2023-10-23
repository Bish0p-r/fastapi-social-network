from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.friendships.router import router as friends_router
from app.blacklist.router import router as blacklist_router
from app.posts.router import router as posts_router
from app.likes.router import router as likes_router
from app.comments.router import router as comments_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(friends_router)
app.include_router(blacklist_router)
app.include_router(posts_router)
app.include_router(likes_router)
app.include_router(comments_router)
