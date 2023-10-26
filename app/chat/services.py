from app.chat.repository import MessagesRepository


class MessagesServices:
    def __init__(self, messages_repository: type[MessagesRepository]):
        self.messages_repository: MessagesRepository = messages_repository()

    def list_of_sent_messages(self, from_user: int, to_user: int):
        return self.messages_repository.list_of_sent_messages(from_user=from_user, to_user=to_user)

    def add_message(self, from_user: int, to_user: int, content: str):
        return self.messages_repository.add(from_user=from_user, to_user=to_user, content=content)
