from http import HTTPStatus

from app.actions.applications.exceptions import ApplicationNotFound
from app.actions.chats.main import create_chat_by_app
from app.actions.chats.models import ChatCreate
from app.models.db.chats import ChatModel
from fastapi import APIRouter
from fastapi import HTTPException

router = APIRouter()


@router.post("/", status_code=HTTPStatus.CREATED)
async def create_chat(chat: ChatCreate):
    try:
        chat = await create_chat_by_app(chat.app_token)
        return chat.model_dump(exclude=["id", "created_at", "updated_at"])
    except ApplicationNotFound:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Application not found"
        )
