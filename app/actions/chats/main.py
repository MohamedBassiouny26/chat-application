import uuid
from random import randint

from app.actions.chats.models import Chat
from app.models.db.chats import ChatModel
from app.providers.redis import RedisConnection


async def create_chat_by_app(app_token: str) -> Chat:
    redis = await RedisConnection.create_connection()
    key = _get_app_chats_count(app_token)
    count = await redis.incr(key)
    chat = Chat(number=count, app_token=app_token)
    await ChatModel.create_chat(chat)
    return chat


def _get_app_chats_count(app_token: str) -> str:
    return f"applications:{app_token}:chats"
