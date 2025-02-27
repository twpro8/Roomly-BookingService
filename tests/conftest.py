# ruff: noqa: E402
import pytest
from unittest import mock

from src.schemas.facilities import FacilityAddRequestDTO

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda func: func).start()


import json

from httpx import AsyncClient, ASGITransport

from src import settings
from src.api.dependencies import get_db
from src.database import Base, null_pool_engine, null_pool_session_maker
from src.models import *  # noqa
from src.schemas.hotels import HotelAddDTO
from src.schemas.rooms import RoomAddDTO
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

    hotels_data = [HotelAddDTO.model_validate(hotel) for hotel in read_json("mock_hotels")]
    rooms_data = [RoomAddDTO.model_validate(room) for room in read_json("mock_rooms")]
    facilities_data = [
        FacilityAddRequestDTO.model_validate(facility) for facility in read_json("mock_facilities")
    ]

    async with DBManager(session_factory=null_pool_session_maker) as db_:
        await db_.hotels.add_bulk(hotels_data)
        await db_.rooms.add_bulk(rooms_data)
        await db_.facilities.add_bulk(facilities_data)
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
            "email": "imagination@no.com",
            "password": "hard_password",
        },
    )


@pytest.fixture(scope="session")
async def authed_ac(register_user, ac):
    res = await ac.post(
        "/users/login",
        json={
            "username": "tester1",
            "password": "hard_password",
        },
    )
    assert res.status_code == 200
    assert ac.cookies["access_token"]
    yield ac


def read_json(file_name: str) -> dict:
    path = f"tests/{file_name}.json"
    with open(path, encoding="utf-8") as file_in:
        return json.load(file_in)
