from app.utils.repository import BaseRepository
from app.posts.models import Posts


class PostsRepository(BaseRepository):
    model = Posts
