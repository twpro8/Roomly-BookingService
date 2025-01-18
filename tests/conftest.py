import time

import pytest
import aiofiles
import json

from httpx import AsyncClient, ASGITransport

from src import settings
from src.database import Base, null_pool_engine
from src.main import app
from src.models import * # import metadata


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with null_pool_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        await client.post(
            "/users/register",
            json={
                "username": "tester1",
                "email": "kot@pes.com",
                "password": "password_<PASSWORD>",
            }
        )


async def read_json(file_name: str) -> dict:
    path = f"tests/{file_name}.json"
    async with (aiofiles.open(path, "rt") as fin):
            res = await fin.read()
            return json.loads(res)


@pytest.fixture(scope="session", autouse=True)
async def add_hotels(setup_database):
    hotels_to_add = await read_json("mock_hotels")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        for hotel in hotels_to_add:
            await client.post("/hotels", json=hotel)


@pytest.fixture(scope="session", autouse=True)
async def add_facilities(setup_database):
    facilities_to_add = await read_json("mock_facilities")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        for facility in facilities_to_add:
            await client.post("/facilities", json=facility)


@pytest.fixture(scope="session", autouse=True)
async def add_rooms(add_hotels, add_facilities):
    rooms_to_add = await read_json("mock_rooms")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        for room in rooms_to_add:
            await client.post(f"/hotels/{room.get('hotel_id')}/rooms", json=room)
