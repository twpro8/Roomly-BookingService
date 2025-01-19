import pytest
import json

from httpx import AsyncClient, ASGITransport

from src import settings
from src.api.dependencies import get_db
from src.database import Base, null_pool_engine, null_pool_session_maker
from src.models import * # import metadata
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager
from src.main import app


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool() -> DBManager:
    async with DBManager(session_factory=null_pool_session_maker) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> DBManager:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with null_pool_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    hotels_data = [HotelAdd.model_validate(hotel) for hotel in read_json("mock_hotels")]
    rooms_data = [RoomAdd.model_validate(room) for room in read_json("mock_rooms")]

    async with DBManager(session_factory=null_pool_session_maker) as db_:
        await db_.hotels.add_bulk(hotels_data)
        await db_.rooms.add_bulk(rooms_data)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


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


def read_json(file_name: str) -> dict:
    path = f"tests/{file_name}.json"
    with open(path, encoding="utf-8") as fin:
        return json.load(fin)
