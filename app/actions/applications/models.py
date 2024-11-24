from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Application(BaseModel):
    name: str
    token: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    chats_count: Optional[int] = None


class ApplicationUpdate(BaseModel):
    name: str


class ApplicationCreate(BaseModel):
    name: str
