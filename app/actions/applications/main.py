import uuid

from app.actions.applications.models import Application
from app.actions.applications.models import ApplicationUpdate
from app.models.db.applications import ApplicationModel


async def add_application(name: str) -> Application:
    token = str(uuid.uuid4())
    app = Application(name=name, token=token)
    await ApplicationModel.add_application(app)
    return app


async def update_application(
    app_token: str, application_update: ApplicationUpdate
) -> Application:
    return await ApplicationModel.update_application(app_token, application_update)


async def get_application_by_token(token: str) -> Application:
    return await ApplicationModel.fetch_application(token)
