import pytest

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
