from datetime import datetime

from app.actions.applications.models import Application
from app.actions.applications.models import ApplicationCreate
from app.models.db.applications import ApplicationModel
from fastapi import APIRouter

router = APIRouter()


@router.get("/{app_token}")
async def fetch_app(app_token: str):
    return app_token


@router.post("/")
async def create_app(application: ApplicationCreate):
    await ApplicationModel.add_application(
        Application(
            name=application.name,
            token="eed",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
    )


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
