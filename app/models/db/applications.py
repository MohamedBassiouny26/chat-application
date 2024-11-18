from typing import List
from typing import Optional

from app.actions.applications.models import Application
from app.actions.applications.models import ApplicationUpdate
from app.providers.db import db
from app.providers.db import metadata
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table

application_table = Table(
    "applications",
    metadata,
    Column("id", Integer, nullable=False, primary_key=True),
    Column("token", String(200), nullable=False, unique=True),
    Column("name", String(200), nullable=False),
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
    async def fetch_applications() -> List[Application]:
        query = application_table.select()
        applications = await db.fetch_all(query=query)
        return [Application(**dict(application)) for application in applications]

    @staticmethod
    async def fetch_application(app_token: str) -> Optional[Application]:
        query = application_table.select().where(application_table.c.token == app_token)
        application = await db.fetch_one(query=query)
        return Application(**dict(application)) if application else None

    @staticmethod
    async def add_application(new_application: Application) -> Optional[Application]:
        query = application_table.insert().values(
            **new_application.model_dump(exclude_unset=True, exclude_none=True)
        )
        await db.execute(query=query)

    @staticmethod
    async def update_application(
        app_token: str, updated_application: ApplicationUpdate
    ) -> Optional[Application]:
        query = (
            application_table.update()
            .where(application_table.c.token == app_token)
            .values(
                **updated_application.model_dump(exclude_unset=True, exclude_none=True)
            )
        )
        await db.execute(query=query)
        query = application_table.select().where(application_table.c.token == app_token)
        application = await db.fetch_one(query=query)
        return Application(**dict(application)) if application else None
