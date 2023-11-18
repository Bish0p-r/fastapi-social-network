import json
from typing import List

from fastapi import WebSocket, APIRouter, Request, WebSocketDisconnect
from starlette.templating import Jinja2Templates

from app.auth.dependencies import GetCurrentUser
from app.chat.dependencies import GetMessagesServices
from app.chat.manager import socket_manager
from app.chat.schemas import MessageSchema
from app.chat.services import MessagesServices
from app.users.models import Users
from app.utils.wrk import get_worker_info


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/{recipient_id}")
async def get(request: Request, recipient_id: int, user: Users = GetCurrentUser):
    # TODO: validation existing user
    return templates.TemplateResponse(
        "chat.html", {"request": request, "user_id": user.id, "recipient_id": recipient_id}
    )


@router.get("/list-of-my-messages-with-user/{user_id}")
async def get_list_of_my_messages_with_user(
    user_id: int, user: Users = GetCurrentUser, messages_services: MessagesServices = GetMessagesServices
) -> List[MessageSchema]:
    return await messages_services.list_of_sent_messages(from_user=user.id, to_user=user_id)


# @router.websocket("/ws/{client_id}/{recipient_id}")
# async def websocket_chat(
#         websocket: WebSocket,
#         client_id: int,
#         recipient_id: int,
#         messages_service=GetMessagesServices,
#         redis=GetRedis
# ):
#     manager = ConnectionManager(redis)
#     await manager.connect(websocket, client_id)
#
#     recent_messages = await messages_service.list_of_sent_messages(from_user=client_id, to_user=recipient_id)
#     if recent_messages:
#         await websocket.send_text("Recent messages:")
#         for message in recent_messages:
#             await websocket.send_text(f"User #{message.from_user} says: {message.content}")
#     await websocket.send_text("New messages:")
#
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await websocket.send_text(f"You wrote: {data}")
#             await messages_service.add_message(from_user=client_id, to_user=recipient_id, content=data)
#             await manager.send_personal_message(f"User #{client_id} says: {data}", recipient_id, client_id)
#     except WebSocketDisconnect:
#         manager.disconnect(client_id)

@router.websocket("/ws/{client_id}/{recipient_id}")
async def websocket_chat(
        websocket: WebSocket,
        client_id: int,
        recipient_id: int,
        messages_service=GetMessagesServices,
):
    # await socket_manager.add_user_to_room(client_id, websocket)
    await socket_manager.create_private_room(client_id, recipient_id, websocket)
    print(f"User #{client_id} WB = {websocket} | Recipient {recipient_id}")
    get_worker_info()

    recent_messages = await messages_service.list_of_sent_messages(from_user=client_id, to_user=recipient_id)
    if recent_messages:
        await websocket.send_text("Recent messages:")
        for message in recent_messages:
            await websocket.send_text(f"User #{message.from_user} says: {message.content}")
    await websocket.send_text("New messages:")

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"You wrote: {data}")
            message = {
                "user_id": client_id,
                "room_id": recipient_id,
                "private_room": (client_id, recipient_id),
                "message": data
            }
            await messages_service.add_message(from_user=client_id, to_user=recipient_id, content=data)
            await socket_manager.broadcast_to_room(f'{(recipient_id, client_id)}', json.dumps(message))
            get_worker_info()

    except WebSocketDisconnect:
        await socket_manager.delete_users_connection(client_id, recipient_id, websocket)
