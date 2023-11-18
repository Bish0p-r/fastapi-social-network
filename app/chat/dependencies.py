from fastapi import Depends

from app.chat.repository import MessagesRepository
from app.chat.services import MessagesServices


async def messages_service():
    return MessagesServices(MessagesRepository)


GetMessagesServices = Depends(messages_service)


# async def get_manager():
#     return ConnectionManager(Get)