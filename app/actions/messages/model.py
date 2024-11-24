from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MessageCreate(BaseModel):
    body: str
    app_token: str
    chat_number: int


class Message(BaseModel):
    id: Optional[int] = None
    body: str
    chat_id: Optional[int] = None
    number: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
