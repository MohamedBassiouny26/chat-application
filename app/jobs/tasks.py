from app.models.db.applications import ApplicationModel
from app.models.db.chats import ChatModel


async def update_chats_count_column():
    print("updating chats count column")
    await ApplicationModel.update_chats_count_col()


async def update_messages_count_column():
    print("updating messages count column")
    await ChatModel.update_messages_count_col()
