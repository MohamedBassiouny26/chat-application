from datetime import datetime
from typing import Optional

from app.actions.messages.model import Message
from pydantic import BaseModel


class Chat(BaseModel):
    id: Optional[int] = None
    number: int
    app_token: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ChatMessages(BaseModel):
    body: str
    number: int
    app_token: str


class ChatCreate(BaseModel):
    app_token: str
