from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Application(BaseModel):
    name: str
    token: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class ApplicationCreate(BaseModel):
    name: str
