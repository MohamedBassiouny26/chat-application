import uuid
from random import randint

from app.actions.chats.models import Chat
from app.models.db.chats import ChatModel


async def create_chat_by_app(app_token: str) -> Chat:
    # TODO: use redis incr to check count and get the new number
    # generate number random
    number = randint(1, 10000)
    chat = Chat(number=number, app_token=app_token)
    await ChatModel.create_chat(chat)
    return chat
