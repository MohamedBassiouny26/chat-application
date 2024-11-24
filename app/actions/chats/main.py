from typing import List

from app.actions.applications.exceptions import ApplicationNotFound
from app.actions.chats.models import Chat
from app.actions.chats.models import ChatMessages
from app.models.db.applications import ApplicationModel
from app.models.db.chats import ChatModel
from app.providers.publisher import ChatCreatedEvent
from app.providers.publisher import publish_to_queue
from app.providers.redis import RedisConnection


async def create_chat_by_app(app_token: str) -> Chat:
    redis = await RedisConnection.create_connection()
    application = await ApplicationModel.fetch_application(app_token)
    if not application:
        raise ApplicationNotFound
    key = _get_app_chats_count_key(app_token)
    count = await redis.incr(key)
    chat = Chat(number=count, app_token=app_token)
    await publish_to_queue(ChatCreatedEvent(**chat.model_dump()))
    return chat


async def get_chats_by_app_token(app_token: str) -> List[ChatMessages]:
    return await ChatModel.fetch_chats_by_app_token(app_token)


def _get_app_chats_count_key(app_token: str) -> str:
    return f"applications:{app_token}:chats"
