from typing import List

from fastapi import WebSocket, APIRouter, Request, WebSocketDisconnect
from starlette.templating import Jinja2Templates

from app.chat.manager import manager
from app.auth.dependencies import GetCurrentUser, get_token, get_current_user
from app.chat.dependencies import GetMessagesServices
from app.chat.services import MessagesServices
from app.users.models import Users
from app.chat.schemas import MessageSchema


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/{recipient_id}")
async def get(
        request: Request,
        recipient_id: int,
        user: Users = GetCurrentUser
):
    return templates.TemplateResponse(
        "chat.html",
        {"request": request, "user_id": user.id, "recipient_id": recipient_id}
    )


@router.get("/list-of-my-messages-with-user/{user_id}")
async def get_list_of_my_messages_with_user(
        user_id: int,
        user: Users = GetCurrentUser,
        messages_services: MessagesServices = GetMessagesServices
) -> List[MessageSchema]:
    return await messages_services.list_of_sent_messages(from_user=user.id, to_user=user_id)


@router.websocket("/ws/{client_id}/{recipient_id}")
async def websocket_chat(
        websocket: WebSocket,
        client_id: int,
        recipient_id: int,
        messages_service=GetMessagesServices
):
    await manager.connect(websocket, client_id)

    recent_messages = await messages_service.list_of_sent_messages(from_user=client_id, to_user=recipient_id)
    if recent_messages:
        await websocket.send_text(f'Recent messages:')
        for message in recent_messages:
            await websocket.send_text(f"User #{message.from_user} says: {message.content}")
    await websocket.send_text(f'New messages:')

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"You wrote: {data}")
            await messages_service.add_message(from_user=client_id, to_user=recipient_id, content=data)
            await manager.send_personal_message(f"User #{client_id} says: {data}", recipient_id, client_id)
    except WebSocketDisconnect:
        manager.disconnect(client_id)
