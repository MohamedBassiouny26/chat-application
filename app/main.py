from app import routers
from app.providers.db import db
from app.providers.redis import RedisConnection
from fastapi import FastAPI

app = FastAPI()


@app.on_event("startup")
async def startup():
    await db.connect()
    await RedisConnection.create_connection()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
    await RedisConnection.close_connection()


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
app.include_router(
    routers.messages,
    prefix="/messages",
    tags=["messages"],
)
