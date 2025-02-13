from typing import Any

import pytest

from httpx import AsyncClient


@pytest.mark.parametrize(
    "hotel_id, date_from, date_to, status_code",
    [
        (1, "2025-07-01", "2025-08-01", 200),
        (1, "2025-07-01", "2025-08-01", 200),
        (1, "2025-08-01", "2025-07-01", 422),
        (1, "2025-08-01", 123, 422),
        (1, "2025-08-01", None, 422),
        (1, None, "2025-08-01", 422),
        (1, None, None, 422),
        (0, "2025-07-01", "2025-08-01", 422),
        (9999999999, "2025-07-01", "2025-08-01", 422),
    ],
)
async def test_get_rooms(
    ac: AsyncClient,
    hotel_id: int,
    date_from: str,
    date_to: str,
    status_code: int,
):
    request_json = {"date_from": date_from, "date_to": date_to}

    response = await ac.get(f"/hotels/{hotel_id}/rooms", params=request_json)
    assert response.status_code == status_code

    if response.status_code == 200:
        rooms = response.json()
        assert len(rooms) == 2


@pytest.mark.parametrize(
    "hotel_id, room_id, status_code",
    [
        (1, 1, 200),
        (1, 2, 200),
        (2, 3, 200),
        (3, 4, 200),
        (4, 5, 404),
        (111, 6, 404),
    ],
)
async def test_get_room(ac: AsyncClient, hotel_id: int, room_id: int, status_code: int):
    response = await ac.get(f"/hotels/{hotel_id}/rooms/{room_id}")
    assert response.status_code == status_code

    if status_code == 200:
        room = response.json()
        assert isinstance(room, dict)
        assert len(room) == 7


@pytest.mark.parametrize(
    "hotel_id, title, description, price, quantity, facilities_ids, status_code, surprise",
    [
        (1, "Free Quero 1", "The best place for you", 1, 5, [], 200, None),
        (1, "Free Quero 1", None, 700, 2, [], 409, None),
        (1, "Free Quero 2", "The best place for you", 1, 5, [], 422, "Surprise!"),
        (1, "Free Quero 3", None, 1, 5, None, 200, None),
        (111, "Free Quero 4", None, 1, 5, None, 404, None),
        (2, "Free Quero 5", None, 0, 5, None, 422, None),
        (2, "Free Quero 5", None, 1, 0, None, 422, None),
    ],
)
async def test_add_room(
    ac: AsyncClient,
    hotel_id: int,
    title: str,
    description: str | None,
    price: int,
    quantity: int,
    facilities_ids: list | None,
    status_code: int,
    surprise: Any | None,
):
    request_json = {"title": title, "price": price, "quantity": quantity}
    if description is not None:
        request_json["description"] = description
    if facilities_ids is not None:
        request_json["facilities_ids"] = facilities_ids
    if surprise is not None:
        request_json["surprise"] = surprise

    response = await ac.post(f"/hotels/{hotel_id}/rooms", json=request_json)
    assert response.status_code == status_code

    # title: str = Field(min_length=5, max_length=50)
    # description: str | None = Field(default=None, min_length=5, max_length=50)
    # price: int = Field(default=888, gt=0, lt=1000000)
    # quantity: int = Field(default=1, gt=0, lt=1000)
    # facilities_ids: list[int] = []
