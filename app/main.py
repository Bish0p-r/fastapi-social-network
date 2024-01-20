from fastapi import FastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from prometheus_fastapi_instrumentator import Instrumentator
from sqladmin import Admin

from app.config import settings
from app.database import async_engine
from app.admin.auth import authentication_backend
from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.friendships.router import router as friends_router
from app.blacklist.router import router as blacklist_router
from app.posts.router import router as posts_router
from app.likes.router import router as likes_router
from app.comments.router import router as comments_router
from app.chat.router import router as chat_router

from app.admin.views import UsersAdmin, PostsAdmin, CommentsAdmin, LikesAdmin, BlacklistsAdmin, FriendshipsAdmin

from app.utils.dependencies import GetRedis

app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(friends_router)
app.include_router(blacklist_router)
app.include_router(posts_router)
app.include_router(likes_router)
app.include_router(comments_router)
app.include_router(chat_router)


admin = Admin(app, async_engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(PostsAdmin)
admin.add_view(CommentsAdmin)
admin.add_view(LikesAdmin)
admin.add_view(BlacklistsAdmin)
admin.add_view(FriendshipsAdmin)


if settings.MODE == "TEST":
    redis = GetRedis
    FastAPICache.init(RedisBackend(redis), prefix="cache", enable=False)


instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)
instrumentator.instrument(app).expose(app)


@app.on_event("startup")
def startup():
    redis = GetRedis
    FastAPICache.init(RedisBackend(redis), prefix="cache")
