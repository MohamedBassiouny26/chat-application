from typing import Optional

from pydantic import BaseModel


class MessageCreate(BaseModel):
    body: str
    app_token: str
    chat_number: int


class Message(BaseModel):
    body: str
    chat_id: Optional[int] = None
    number: int
