import os

import aio_pika
from app.actions.chats.models import Chat
from app.actions.messages.model import Message
from pydantic import BaseModel


class Event(BaseModel):
    event_name: str


class MessageCreatedEvent(Event, Message):
    event_name: str = "chats/new_message_created"


class ChatCreatedEvent(Event, Chat):
    event_name: str = "chats/new_chat_created"


async def publish_to_queue(message: Event):
    host = os.getenv("RABBIT_MQ_HOST", "localhost")
    port = os.getenv("RABBIT_MQ_PORT", "5672")
    connection_url = f"amqp://guest:guest@{host}:{port}/"
    connection = await aio_pika.connect_robust(connection_url)
    async with connection:
        channel = await connection.channel()

        queue_name = "db_tasks_queue"
        await channel.declare_queue(queue_name, durable=True)

        payload = message.model_dump_json()

        await channel.default_exchange.publish(
            aio_pika.Message(
                body=payload.encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,  # Make message persistent
            ),
            routing_key=queue_name,
        )
        print(f"Message published: {payload}")
