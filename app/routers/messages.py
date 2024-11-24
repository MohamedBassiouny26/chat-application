from http import HTTPStatus

from app.actions.chats.exceptions import ChatNotFoundException
from app.actions.messages.main import create_message as create_message_action
from app.actions.messages.model import MessageCreate
from app.models.db.chats import ChatModel
from app.providers.elastic_search import ElasticSearch
from fastapi import APIRouter
from fastapi import HTTPException

router = APIRouter()


@router.post("/", status_code=HTTPStatus.CREATED)
async def create_message(message: MessageCreate):
    try:
        message = await create_message_action(message)
        return message.model_dump(exclude=["id", "chat_id"])
    except ChatNotFoundException:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Chat not found")


@router.get("/search/{app_token}/chat_number")
async def search_messages(app_token: str, chat_number: int, query: str):
    try:
        chat = await ChatModel.fetch_chat(app_token=app_token, number=chat_number)
        es = await ElasticSearch.create_connection()
        result = await es.search(
            index=ElasticSearch.__INDEX_NAME__,
            body={
                "query": {
                    "bool": {
                        "must": [
                            {"term": {"chat_id": chat.id}},
                            {"match": {"body": query}},
                        ]
                    }
                }
            },
        )
        messages = [
            {"id": hit["_id"], **hit["_source"]} for hit in result["hits"]["hits"]
        ]
        return {"messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
