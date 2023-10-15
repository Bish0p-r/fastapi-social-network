from app.common.repository import BaseRepository
from app.users.models import Users


class UserRepository(BaseRepository):
    model = Users
