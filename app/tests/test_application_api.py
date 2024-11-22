from http import HTTPStatus

import pytest
from app.models.db.applications import application_table


@pytest.mark.asyncio
async def test_fetch_app(client, create_dummy_records):
    await create_dummy_records(
        [{"name": "Test App", "token": "test_token"}], application_table
    )
    response = await client.get("/applications/test_token")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["token"] == "test_token"


@pytest.mark.asyncio
async def test_create_app(client):
    body = {"name": "Test App"}
    response = await client.post("/applications/", json=body)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["name"] == "Test App"
    assert response.json()["token"]


@pytest.mark.asyncio
async def test_update_app(client, create_dummy_records):
    await create_dummy_records(
        [{"name": "Test App", "token": "test_token"}], application_table
    )
    body = {"name": "Prod App"}
    response = await client.patch("/applications/test_token", json=body)
    assert response.status_code == HTTPStatus.OK
    assert response.json()["name"] == "Prod App"


@pytest.mark.asyncio
async def test_update_app_not_found(client, create_dummy_records):
    await create_dummy_records(
        [{"name": "Test App", "token": "test_token"}], application_table
    )
    body = {"name": "Prod App"}
    response = await client.patch("/applications/test_not_found", json=body)
    assert response.status_code == HTTPStatus.NOT_FOUND
