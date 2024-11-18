from typing import Optional

from app.actions.applications.models import Application
from app.providers.db import db
from app.providers.db import metadata
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import String
from sqlalchemy import Table

application_table = Table(
    "applications",
    metadata,
    Column("id", String, nullable=False, primary_key=True),
    Column("token", String, nullable=False, unique=True),
    Column("name", String, nullable=False),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
    Column(
        "updated_at",
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    ),
)


class ApplicationModel:
    @staticmethod
    async def fetch_application(app_token: str) -> Optional[Application]:
        query = application_table.select().where(
            application_table.c.app_token == app_token
        )
        application = await db.fetch_one(query=query)
        return Application(**application) if application else None

    @staticmethod
    async def add_application(new_application: Application) -> Optional[Application]:
        query = application_table.insert().values(
            **new_application.model_dump(exclude_unset=True, exclude_none=True)
        )
        application = await db.fetch_one(query=query)
        return Application(**application) if application else None
