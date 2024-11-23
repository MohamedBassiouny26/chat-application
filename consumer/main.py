import asyncio
import json
import multiprocessing
import os

import aio_pika
from aio_pika import IncomingMessage
from app.actions.chats.models import Chat
from app.actions.messages.model import Message
from app.models.db.chats import ChatModel
from app.models.db.messages import MessageModel
from app.providers.db import db


async def consume_message(event: IncomingMessage):
    async with event.process():
        print(f"Consumed message: {event.body.decode()}")
        json_event = json.loads(event.body.decode())
        event_name = json_event["event_name"]
        if event_name == "chats/new_message_created":
            message = Message(**json_event)
            await MessageModel.create_message(
                chat_id=message.chat_id,
                body=message.body,
                message_number=message.number,
            )
        elif event_name == "chats/new_chat_created":
            chat = Chat(**json_event)
            await ChatModel.create_chat(chat)


async def consume_from_queue():
    host = os.getenv("RABBIT_MQ_HOST", "localhost")
    port = os.getenv("RABBIT_MQ_PORT", "5672")

    connection_url = f"amqp://guest:guest@{host}:{port}/"

    connection = await aio_pika.connect_robust(connection_url)
    async with connection:
        channel = await connection.channel()

        queue_name = "db_tasks_queue"
        queue = await channel.declare_queue(queue_name, durable=True)

        async for message in queue:
            await consume_message(message)


def start_consumer():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(db.connect())
    loop.run_until_complete(consume_from_queue())


if __name__ == "__main__":
    start_consumer()
