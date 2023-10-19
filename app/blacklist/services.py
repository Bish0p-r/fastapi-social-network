from app.blacklist.repository import BlacklistRepository


class BlacklistServices:
    def __init__(self, user_repository: type[BlacklistRepository]):
        self.blacklist_repository: BlacklistRepository = blacklist_repository()
