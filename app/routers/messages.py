from http import HTTPStatus

from app.actions.messages.main import create_message as create_message_action
from app.actions.messages.model import MessageCreate
from app.models.db.chats import ChatModel
from fastapi import APIRouter

router = APIRouter()


@router.post("/", status_code=HTTPStatus.CREATED)
async def create_message(message: MessageCreate):
    message = await create_message_action(message)
    return message.model_dump(exclude=["id", "chat_id"])


@router.get("")
async def get_all_apps():
    return await ChatModel.fetch_all_chats()
