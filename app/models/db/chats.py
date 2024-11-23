from operator import and_
from typing import List
from typing import Optional

from app.actions.chats.models import Chat
from app.providers.db import db
from app.providers.db import metadata
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
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
    async def fetch_chats_by_app_token(app_token) -> List[Chat]:
        query = chat_table.select().where(chat_table.c.app_token == app_token)
        chats = await db.fetch_all(query=query)
        return [Chat(**dict(chat)) for chat in chats]

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
