from http import HTTPStatus
from typing import List

from app.actions.applications.main import create_application
from app.actions.applications.main import get_application_by_token
from app.actions.applications.main import update_application
from app.actions.applications.models import Application
from app.actions.applications.models import ApplicationCreate
from app.actions.applications.models import ApplicationUpdate
from app.actions.chats.main import get_chats_by_app_token
from app.actions.chats.models import Chat
from app.actions.chats.models import ChatMessages
from app.models.db.applications import ApplicationModel
from fastapi import APIRouter
from fastapi import HTTPException

router = APIRouter()


@router.get("/{app_token}", response_model=Application, status_code=HTTPStatus.OK)
async def fetch_app(app_token: str):
    return await get_application_by_token(app_token)


@router.get(
    "/{app_token}/chats", response_model=List[ChatMessages], status_code=HTTPStatus.OK
)
async def fetch_app_chats(app_token: str):
    app_chats = await get_chats_by_app_token(app_token)
    return [
        chat.model_dump(exclude_none=True, exclude_unset=True) for chat in app_chats
    ]


@router.post("/", status_code=HTTPStatus.CREATED, response_model=Application)
async def create_app(application: ApplicationCreate):
    return await create_application(application.name)


@router.patch("/{app_token}", response_model=Application)
async def update_app(app_token: str, application_update: ApplicationUpdate):
    try:
        return await update_application(app_token, application_update)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)


# FIXME: this should be removed just for testing
@router.get("")
async def get_all_apps():
    return await ApplicationModel.fetch_applications()
