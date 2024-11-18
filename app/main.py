from app import routers
from app.providers.db import db
from fastapi import FastAPI

app = FastAPI()


@app.on_event("startup")
async def startup():
    await db.connect()


app.include_router(
    routers.application,
    prefix="/applications",
    tags=["applications"],
)

app.include_router(
    routers.chat,
    prefix="/chats",
    tags=["chats"],
)
