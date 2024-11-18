from http import HTTPStatus

from app.actions.applications.main import update_application
from app.actions.applications.models import Application
from app.actions.applications.models import ApplicationCreate
from app.actions.applications.models import ApplicationUpdate
from app.actions.chats.main import create_chat_by_app
from app.actions.chats.models import ChatCreate
from app.models.db.applications import ApplicationModel
from app.models.db.chats import ChatModel
from fastapi import APIRouter

router = APIRouter()


# @router.get("/{app_token}", response_model=Application, status_code=HTTPStatus.OK)
# async def fetch_app(app_token: str):
#     return await get_application_by_token(app_token)


@router.post("/", status_code=HTTPStatus.CREATED)
async def create_chat(chat: ChatCreate):
    return await create_chat_by_app(chat.app_token)


@router.patch("/{app_token}")
async def update_app(app_token: str, application_update: ApplicationUpdate):
    return await update_application(app_token, application_update)


# FIXME: this should be removed just for testing


@router.get("")
async def get_all_apps():
    return await ChatModel.fetch_all_chats()
