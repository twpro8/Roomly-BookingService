from datetime import date

import pytest
from typing import Any
from pydantic import ValidationError

from src.database import null_pool_engine
from src.schemas.bookings import Booking
from src.models import BookingsORM


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code, unexpected_field",
    [
        (1, "2025-09-01", "2025-09-10", 200, None),
        (1, "2025-09-01", "2025-09-10", 200, None),
        (1, "2025-09-01", "2025-09-10", 409, None),
        (1, "2025-09-11", "2025-09-20", 200, None),
        (1, "2025-09-11", "2025-09-20", 200, None),
        (1, "2025-09-11", "2025-09-20", 409, None),
        (2, "2025-09-01", "2025-09-10", 200, None),
        (2, "2025-09-01", "2025-09-10", 200, None),
        (2, "2025-09-01", "2025-09-10", 409, None),
        (2, "2025-09-11", "2025-09-20", 200, None),
        (2, "2025-09-11", "2025-09-20", 200, None),
        (2, "2025-09-11", "2025-09-20", 409, None),
        (2, "2025-09-21", "2025-09-30", 422, "unexpected_field"),
        (-1, "2025-09-21", "2025-09-30", 422, None),
        (0, "2025-09-21", "2025-09-30", 422, None),
        (2147483647, "2025-09-21", "2025-09-30", 422, None),
        (3, "2025-09-01", "2025-09-32", 422, None),
        (111, "2025-09-01", "2025-09-30", 404, None),
        (222, "2025-09-01", "2025-09-30", 404, None),
        (333, "2025-09-01", "2025-09-30", 404, None),
    ],
)
async def test_add_booking(
    db,
    authed_ac,
    room_id: int | None,
    date_from: date | None,
    date_to: date | None,
    status_code: int,
    unexpected_field: Any | None,
):
    request_json = {}
    if room_id is not None:
        request_json["room_id"] = room_id
    if date_from is not None:
        request_json["date_from"] = date_from
    if date_to is not None:
        request_json["date_to"] = date_to
    if unexpected_field is not None:
        request_json["unexpected_field"] = unexpected_field

    response = await authed_ac.post("/bookings", json=request_json)
    assert response.status_code == status_code

    if response.status_code == 200:
        response_json = response.json()
        assert isinstance(response_json, dict)
        assert response_json["status"] == "ok"
        assert "data" in response_json

        try:
            Booking(**response_json["data"])
        except ValidationError as e:
            assert False, f"Booking data validation failed: {e}"


@pytest.fixture(scope="module")
async def delete_all_bookings():
    """Function recreates bookings table"""
    async with null_pool_engine.begin() as conn:
        await conn.run_sync(BookingsORM.__table__.drop)
        await conn.run_sync(BookingsORM.__table__.create)


@pytest.mark.parametrize(
    "room_id, date_from, date_to, case, status_code",
    [
        (1, "2025-09-01", "2025-09-05", 1, 200),
        (1, "2025-09-01", "2025-09-05", 2, 200),
        (1, "2025-09-01", "2025-09-05", 3, 409),
        (2, "2025-09-01", "2025-09-05", 3, 200),
        (2, "2025-09-01", "2025-09-05", 4, 200),
        (2, "2025-09-01", "2025-09-05", 5, 409),
        (3, "2025-09-01", "2025-09-05", 5, 200),
        (3, "2025-09-01", "2025-09-05", 6, 200),
        (3, "2025-09-01", "2025-09-05", 7, 409),
    ],
)
async def test_add_and_get_my_bookings(
    case, room_id, date_from, date_to, status_code, delete_all_bookings, authed_ac
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
    assert response.status_code == status_code

    if response.status_code == 200:
        # Get my bookings
        result = await authed_ac.get("/bookings/me")

        assert response.status_code == 200
        assert result.status_code == 200
        assert isinstance(response.json(), dict)
        assert isinstance(result.json(), list)
        assert len(result.json()) == case


@pytest.mark.parametrize(
    "booking_id, status_code",
    [
        (1, 200),
        (2, 200),
        (3, 200),
        (333, 404),
        (-1, 422),
        (0, 422),
        (9999999999, 422),
    ],
)
async def test_delete_booking(authed_ac, booking_id: int, status_code: int):
    response = await authed_ac.delete(f"/bookings/{booking_id}")
    assert response.status_code == status_code

    if response.status_code == 200:
        current_bookings = await authed_ac.get("/bookings/me")
        assert current_bookings.status_code == 200
        assert isinstance(current_bookings.json(), list)

        is_deleted = next(
            (booking for booking in current_bookings.json() if booking["id"] == booking_id), None
        )
        assert is_deleted is None, (
            f"Facility with id {booking_id} was not deleted or still exists in the list"
        )
