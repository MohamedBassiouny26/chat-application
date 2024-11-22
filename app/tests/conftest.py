from typing import Dict
from typing import List

import pytest
import pytest_asyncio
from app.main import app  # Import your FastAPI app
from app.models.db.applications import application_table
from app.providers.db import db
from httpx import AsyncClient
from sqlalchemy import Table

db_tables = [application_table]


@pytest_asyncio.fixture()
async def client():
    if not db.is_connected:
        await db.connect()
        [await db.execute(table.delete()) for table in db_tables]
    async with AsyncClient(app=app, base_url="http://") as client:
        yield client
    [await db.execute(query=table.delete()) for table in db_tables]
    if db.is_connected:
        await db.disconnect()


@pytest_asyncio.fixture()
async def create_dummy_records():
    async def insert_records(records: List[Dict], model: Table):
        query = model.insert()
        results = []
        print("records", records)
        for record in records:
            result = await db.fetch_one(query=query, values=record)
            results.append(result)
        return results

    return insert_records
