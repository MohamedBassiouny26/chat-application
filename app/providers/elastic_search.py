from app.actions.messages.model import Message
from elasticsearch import AsyncElasticsearch


class ElasticSearch:
    __CONNECTION__ = None
    __INDEX_NAME__ = "messages"

    @staticmethod
    async def create_connection():
        if not ElasticSearch.__CONNECTION__ or not ElasticSearch.__CONNECTION__.exists:
            ElasticSearch.__CONNECTION__ = AsyncElasticsearch(
                "http://elasticsearch:9200",  # Use HTTPS if your Elasticsearch is configured that way
            )
        try:
            health = await ElasticSearch.__CONNECTION__.cluster.health()
        except Exception as e:
            print("Error connecting to Elasticsearch:", e)
        return ElasticSearch.__CONNECTION__

    @staticmethod
    async def create_index():
        es = await ElasticSearch.create_connection()
        if not await es.indices.exists(index=ElasticSearch.__INDEX_NAME__):
            await es.indices.create(
                index=ElasticSearch.__INDEX_NAME__,
                body={
                    "mappings": {
                        "properties": {
                            "body": {"type": "text"},
                            "chat_id": {"type": "keyword"},
                            "created_at": {"type": "date"},
                        }
                    }
                },
            )

    @staticmethod
    async def add_message_index(message: Message):
        es = await ElasticSearch.create_connection()
        await es.index(
            index=ElasticSearch.__INDEX_NAME__,
            id=message.id,
            document={
                "body": message.body,
                "chat_id": message.chat_id,
                "created_at": message.created_at,
            },
        )
