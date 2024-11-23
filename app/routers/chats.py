from http import HTTPStatus

from app.actions.chats.main import create_chat_by_app
from app.actions.chats.models import ChatCreate
from app.models.db.chats import ChatModel
from fastapi import APIRouter

router = APIRouter()


@router.post("/", status_code=HTTPStatus.CREATED)
async def create_chat(chat: ChatCreate):
    chat = await create_chat_by_app(chat.app_token)
    return chat.model_dump(exclude=["id", "created_at", "updated_at"])
