import pytest

from src.database import null_pool_engine
from src.models import BookingsORM


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2025-09-01", "2025-09-10", 200),
        (1, "2025-09-02", "2025-09-11", 200),
        (1, "2025-09-03", "2025-09-12", 200),
        (1, "2025-09-04", "2025-09-13", 200),
        (1, "2025-09-05", "2025-09-14", 200),
        (1, "2025-09-06", "2025-09-15", 409),
        (1, "2025-09-07", "2025-09-16", 409),
        (1, "2025-10-01", "2025-10-10", 200),
        (1, "2025-10-02", "2025-10-11", 200),
    ],
)
async def test_add_booking(room_id, date_from, date_to, status_code, db, authed_ac):
    # room_id = (await db.rooms.get_all())[0].id
    res = await authed_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert res.status_code == status_code
    if status_code == 200:
        res = res.json()
        assert isinstance(res, dict)
        assert res["status"] == "ok"
        assert "data" in res


@pytest.fixture(scope="module")
async def delete_all_bookings():
    """Function recreates bookings table"""
    async with null_pool_engine.begin() as conn:
        await conn.run_sync(BookingsORM.__table__.drop)
        await conn.run_sync(BookingsORM.__table__.create)


@pytest.mark.parametrize(
    "room_id, date_from, date_to, case",
    [
        (1, "2025-09-01", "2025-09-05", 1),
        (1, "2025-09-10", "2025-09-15", 2),
        (1, "2025-09-20", "2025-09-25", 3),
    ],
)
async def test_add_and_get_my_bookings(
    case, room_id, date_from, date_to, delete_all_bookings, authed_ac
):
    # Add a booking
    response = await authed_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    # Get my bookings
    result = await authed_ac.get("/bookings/me")

    assert response.status_code == 200
    assert result.status_code == 200
    assert isinstance(response.json(), dict)
    assert isinstance(result.json(), list)
    assert len(result.json()) == case
