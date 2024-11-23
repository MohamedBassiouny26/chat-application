from collections import defaultdict
from operator import and_
from typing import List
from typing import Optional

from app.actions.chats.models import Chat
from app.actions.chats.models import ChatMessages
from app.actions.messages.model import Message
from app.models.db.messages import message_table
from app.providers.db import db
from app.providers.db import metadata
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import select
from sqlalchemy import String
from sqlalchemy import Table

chat_table = Table(
    "chats",
    metadata,
    Column("id", Integer, nullable=False, primary_key=True),
    Column(
        "app_token",
        String(200),
        ForeignKey("applications.token", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("number", Integer, nullable=False),
    Column("messages_count", Integer, nullable=True, default=0),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
    Column(
        "updated_at",
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    ),
)


class ChatModel:
    @staticmethod
    async def fetch_chats_by_app_token(app_token) -> List[ChatMessages]:
        query = (
            select(
                chat_table.c.number,
                message_table.c.number.label("message_number"),
                message_table.c.body,
                chat_table.c.app_token,
            )
            .join(
                message_table, message_table.c.chat_id == chat_table.c.id, isouter=True
            )
            .where(chat_table.c.app_token == app_token)
            .order_by(chat_table.c.created_at.desc())
        )
        chats = defaultdict(lambda: {"messages": []})
        results = await db.fetch_all(query=query)
        for row in results:
            chat_number = row["number"]
            app_token = row["app_token"]
            message_body = row["body"]
            message_number = row["message_number"]

            chats[chat_number]["chat_number"] = chat_number
            chats[chat_number]["app_token"] = app_token
            if message_body:
                chats[chat_number]["messages"].append(
                    {"body": message_body, "message_number": message_number}
                )
        chats_messages = []
        for key, value in chats.items():
            messages = value.get("messages")
            chat_number = value.get("chat_number")
            app_token = value.get("app_token")
            chat = Chat(number=chat_number, app_token=app_token)
            messages = [
                Message(body=message["body"], number=message["message_number"])
                for message in messages
            ]
            chats_messages.append(ChatMessages(chat=chat, messages=messages))

        return chats_messages

    @staticmethod
    async def fetch_chat(app_token: str, number: int) -> Optional[Chat]:
        query = chat_table.select().where(
            and_(chat_table.c.app_token == app_token, chat_table.c.number == number)
        )
        chat = await db.fetch_one(query=query)
        return Chat(**dict(chat)) if chat else None

    @staticmethod
    async def create_chat(chat: Chat):
        query = chat_table.insert().values(
            **chat.model_dump(exclude_unset=True, exclude_none=True)
        )
        await db.execute(query=query)

    @staticmethod
    async def fetch_all_chats() -> List[Chat]:
        query = chat_table.select()
        chats = await db.fetch_all(query=query)
        return [Chat(**dict(chat)) for chat in chats]
