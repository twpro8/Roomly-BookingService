import pytest
import aiofiles
import json

from httpx import AsyncClient, ASGITransport

from src import settings
from src.database import Base, null_pool_engine, null_pool_session_maker
from src.models import * # import metadata
from src.utils.db_manager import DBManager
from src.main import app

@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture()
async def db() -> DBManager:
    async with DBManager(session_factory=null_pool_session_maker) as db:
        yield db


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with null_pool_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database, ac):
    await ac.post(
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
async def add_hotels(setup_database, ac):
    hotels_to_add = await read_json("mock_hotels")
    for hotel in hotels_to_add:
        await ac.post("/hotels", json=hotel)


@pytest.fixture(scope="session", autouse=True)
async def add_facilities(setup_database, ac):
    facilities_to_add = await read_json("mock_facilities")
    for facility in facilities_to_add:
        await ac.post("/facilities", json=facility)


@pytest.fixture(scope="session", autouse=True)
async def add_rooms(add_hotels, add_facilities, ac):
    rooms_to_add = await read_json("mock_rooms")
    for room in rooms_to_add:
        await ac.post(f"/hotels/{room.get('hotel_id')}/rooms", json=room)
