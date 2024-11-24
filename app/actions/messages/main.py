from app.actions.chats.exceptions import ChatNotFoundException
from app.actions.messages.model import Message
from app.actions.messages.model import MessageCreate
from app.models.db.chats import ChatModel
from app.models.db.messages import MessageModel
from app.providers.publisher import MessageCreatedEvent
from app.providers.publisher import publish_to_queue
from app.providers.redis import RedisConnection


async def create_message(message: MessageCreate) -> Message:
    redis = await RedisConnection.create_connection()
    chat = await ChatModel.fetch_chat(message.app_token, message.chat_number)
    if not chat:
        raise ChatNotFoundException
    chat_id = chat.id
    key = _get_message_count_key(chat_id)
    count = await redis.incr(key)
    message = Message(chat_id=chat_id, number=count, body=message.body)
    await publish_to_queue(MessageCreatedEvent(**message.model_dump()))
    return message


def _get_message_count_key(chat_id: int):
    return f"chats:{chat_id}:messages_count"
