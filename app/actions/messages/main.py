from app.actions.messages.model import Message
from app.actions.messages.model import MessageCreate
from app.models.db.chats import ChatModel
from app.models.db.messages import MessageModel
from app.providers.redis import RedisConnection


async def create_message(message: MessageCreate) -> Message:
    redis = await RedisConnection.create_connection()
    chat = await ChatModel.fetch_chat(message.app_token, message.chat_number)
    chat_id = chat.id
    key = _get_message_count_key(chat_id)
    count = await redis.incr(key)
    # TODO: publish message queue
    await MessageModel.create_message(chat_id, message.body, count)
    return Message(chat_id=chat_id, number=count, body=message.body)


def _get_message_count_key(chat_id: int):
    return f"chats:{chat_id}:messages_count"
