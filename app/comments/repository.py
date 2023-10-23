from app.comments.models import Comment
from app.utils.repository import BaseRepository


class CommentsRepository(BaseRepository):
    model = Comment
