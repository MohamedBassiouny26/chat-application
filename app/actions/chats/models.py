from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Chat(BaseModel):
    number: int
    app_token: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ChatCreate(BaseModel):
    app_token: str
