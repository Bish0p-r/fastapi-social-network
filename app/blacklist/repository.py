from app.blacklist.models import Blacklist
from app.utils.repository import BaseRepository


class BlacklistRepository(BaseRepository):
    model = Blacklist
