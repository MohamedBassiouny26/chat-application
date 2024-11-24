from operator import and_
from typing import List
from typing import Optional

from app.actions.chats.models import Chat
from app.actions.messages.model import Message
from app.actions.messages.model import MessageCreate
from app.providers.db import db
from app.providers.db import metadata
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import UniqueConstraint

message_table = Table(
    "messages",
    metadata,
    Column("id", Integer, nullable=False, primary_key=True),
    Column(
        "chat_id",
        Integer,
        ForeignKey("chats.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    ),
    Column("number", Integer, nullable=False),
    Column("body", String(200), nullable=False),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
    Column(
        "updated_at",
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    ),
    UniqueConstraint(
        "chat_id", "number", name="uq_chat_id_number"
    ),  # Composite unique constraint
)


class MessageModel:
    @staticmethod
    async def fetch_message_by_chat_id(chat_id) -> List[Chat]:
        query = message_table.select().where(message_table.c.chat_id == chat_id)
        chats = await db.fetch_all(query=query)
        return [Chat(**dict(chat)) for chat in chats]

    @staticmethod
    async def create_message(chat_id: int, body: str, message_number: int):
        query = message_table.insert().values(
            chat_id=chat_id, body=body, number=message_number
        )
        count = await db.execute(query)
        if count:
            query = message_table.select().where(
                message_table.c.number == message_number
            )
            result = await db.fetch_one(query)
            return Message(**dict(result))
