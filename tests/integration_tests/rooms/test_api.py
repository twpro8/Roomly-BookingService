from typing import Any, List

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
        (1, "Free Quero 01", "The best place for you", 1, 5, [], 200, None),
        (1, "Free Quero 02", "The best place for you", 1, 5, [4, 6, 1, 3], 200, None),
        (1, "Free Quero 03", "The best place for you", 1, 5, [], 200, None),
        (1, "Free Quero 04", "The best place for you", 1, 5, [1, 3, 5], 200, None),
        (1, "Free Quero 05", "The best place for you", 1, 5, [], 200, None),
        (1, "Free Quero 1", None, 700, 2, [], 409, None),
        (1, "Free Quero 2", "The best place for you", 1, 5, [], 422, "Surprise!"),
        (1, "Free Quero 3", None, 1, 5, None, 200, None),
        (111, "Free Quero 4", None, 1, 5, None, 404, None),
        (2, "Free Quero 5", None, 0, 5, None, 422, None),
        (2, "Free Quero 5", None, 1, 0, None, 422, None),
        (2, "Free Quero 6", "The best place for you", 1788, 2, [1, 2, 3, 4, 5], 200, None),
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


@pytest.mark.parametrize(
    """hotel_id,
    room_id,
    new_title,
    new_description,
    new_price,
    new_quantity,
    new_facilities_ids,
    status_code,
    response_json,
    surprise""",
    [
        (
            1,
            1,
            "PUT_New Room Title 1",
            "PUT_New Room Descr.",
            100,
            3,
            [2, 3, 4],
            200,
            {
                "title": "PUT_New Room Title 1",
                "description": "PUT_New Room Descr.",
                "price": 100,
                "quantity": 3,
                "facilities": [
                    {"title": "Air Conditioning", "id": 2},
                    {"title": "Flat-Screen TV", "id": 3},
                    {"title": "Mini Bar", "id": 4},
                ],
            },
            None,
        ),
        (
            1,
            1,
            "PUT_New Title Only",
            None,
            1100,
            2,
            [2, 3, 4],
            200,
            {
                "title": "PUT_New Title Only",
                "price": 1100,
                "quantity": 2,
                "facilities": [
                    {"title": "Air Conditioning", "id": 2},
                    {"title": "Flat-Screen TV", "id": 3},
                    {"title": "Mini Bar", "id": 4},
                ],
            },
            None,
        ),
        (999, 1, "PUT_New Room Title", "PUT_New Room Descr.", 100, 3, [2, 3, 4], 404, None, None),
        (1, 999, "PUT_New Room Title", "PUT_New Room Descr.", 100, 3, [2, 3, 4], 404, None, None),
        (1, 1, "", "PUT_New Room Descr.", 100, 3, [2, 3, 4], 422, None, None),
        (1, 1, "PUT_New Title", "PUT_New Descr.", 1200, 3, [2, 3, 4], 422, None, "Surprise!"),
        (1, 1, "g" * 50, "PUT_New Descr.", 1200, 2, [2, 3, 4], 200, None, None),
        (1, 1, "h" * 51, "PUT_New Descr.", 1200, 2, [2, 3, 4], 422, None, None),
        (1, 1, "PUT_New Title", "s" * 50, 1200, 2, [2, 3, 4], 200, None, None),
        (1, 1, "PUT_New Title", "d" * 51, 1200, 2, [2, 3, 4], 422, None, None),
        (1, 1, "New Room Title", "New Room Descr.", -100, 3, [2, 3, 4], 422, None, None),
        (1, 1, None, None, 1300, 3, [2, 3, 4], 422, None, None),
        (1, 1, "New Room Title", "New Room Descr.", 100, 3, ["not_an_int", 3, 4], 422, None, None),
    ],
)
async def test_edit_room(
    ac: AsyncClient,
    hotel_id: int,
    room_id: int,
    new_title: str,
    new_description: str | None,
    new_price: int,
    new_quantity: int,
    new_facilities_ids: List[int] | None,
    status_code: int,
    response_json: Any | None,
    surprise: Any | None,
):
    request_json = {"title": new_title, "price": new_price, "quantity": new_quantity}
    if new_description is not None:
        request_json["description"] = new_description
    if new_facilities_ids is not None:
        request_json["facilities_ids"] = new_facilities_ids
    if surprise is not None:
        request_json["surprise"] = surprise

    response = await ac.put(f"/hotels/{hotel_id}/rooms/{room_id}", json=request_json)

    assert response.status_code == status_code

    if status_code == 200:
        room_response = await ac.get(f"/hotels/{hotel_id}/rooms/{room_id}")
        assert room_response.status_code == 200
        updated_room_data = room_response.json()

        if response_json:
            for key, value in response_json.items():
                assert updated_room_data.get(key) == value

    elif response_json:
        assert response.json() == response_json


@pytest.mark.parametrize(
    """hotel_id,
    room_id,
    new_title,
    new_description,
    new_price,
    new_quantity,
    new_facilities_ids,
    status_code,
    response_json,
    surprise""",
    [
        (
            2,
            3,
            "New Room Title 1",
            "New Room Descr.",
            100,
            3,
            [2, 3, 4],
            200,
            {
                "title": "New Room Title 1",
                "description": "New Room Descr.",
                "price": 100,
                "quantity": 3,
                "facilities": [
                    {"title": "Air Conditioning", "id": 2},
                    {"title": "Flat-Screen TV", "id": 3},
                    {"title": "Mini Bar", "id": 4},
                ],
            },
            None,
        ),
        (2, 3, "New Title Only", None, None, None, None, 200, {"title": "New Title Only"}, None),
        (
            2,
            3,
            None,
            "New Description Only",
            None,
            None,
            None,
            200,
            {"description": "New Description Only"},
            None,
        ),
        (2, 3, None, None, 200, None, None, 200, {"price": 200}, None),
        (2, 3, None, None, None, 5, None, 200, {"quantity": 5}, None),
        (
            999,
            4,
            "New Title",
            "New Description",
            100,
            3,
            [2, 3, 4],
            404,
            {"detail": "Hotel not found"},
            None,
        ),
        (
            1,
            999,
            "New Title",
            "New Description",
            100,
            3,
            [2, 3, 4],
            404,
            {"detail": "Room not found"},
            None,
        ),
        (2, 3, "", "New Description", 100, 3, [2, 3, 4], 422, None, None),
        (2, 3, "New Title", "New Description", -100, 3, [2, 3, 4], 422, None, None),
        (2, 3, None, None, None, None, None, 422, None, None),
        (2, 3, "New Title", "New Description", 100, 3, ["not_an_int", 3, 4], 422, None, None),
        (2, 3, "New Title", "New Description", 100, 3, [2, 3, 4], 422, None, "Boooo!"),
        (2, 3, "1" * 50, None, None, None, None, 200, None, None),
        (2, 3, "2" * 51, None, None, None, None, 422, None, None),
        (2, 3, None, "3" * 50, None, None, None, 200, None, None),
        (2, 3, None, "4" * 51, None, None, None, 422, None, None),
        (0, 3, "New Title", "New Description", 100, 3, [2, 3, 4], 422, None, None),
        (2, 0, "New Title", "New Description", 100, 3, [2, 3, 4], 422, None, None),
        (9999999999, 3, "New Title", "New Description", 100, 3, [2, 3, 4], 422, None, None),
        (2, 9999999999, "New Title", "New Description", 100, 3, [2, 3, 4], 422, None, None),
        (
            2,
            3,
            "Just New Title",
            "Just New Descr.",
            100,
            3,
            [2, 3, 4],
            200,
            {
                "title": "Just New Title",
                "description": "Just New Descr.",
                "price": 100,
                "quantity": 3,
                "facilities": [
                    {"title": "Air Conditioning", "id": 2},
                    {"title": "Flat-Screen TV", "id": 3},
                    {"title": "Mini Bar", "id": 4},
                ],
            },
            None,
        ),
    ],
)
async def test_partly_edit_room(
    ac: AsyncClient,
    hotel_id: int,
    room_id: int,
    new_title: str | None,
    new_description: str | None,
    new_price: int | None,
    new_quantity: int | None,
    new_facilities_ids: List[int] | None,
    status_code: int,
    response_json: Any | None,
    surprise: Any | None,
):
    request_json = {}
    if new_title is not None:
        request_json["title"] = new_title
    if new_description is not None:
        request_json["description"] = new_description
    if new_price is not None:
        request_json["price"] = new_price
    if new_quantity is not None:
        request_json["quantity"] = new_quantity
    if new_facilities_ids is not None:
        request_json["facilities_ids"] = new_facilities_ids
    if surprise is not None:
        request_json["surprise"] = surprise

    response = await ac.patch(f"/hotels/{hotel_id}/rooms/{room_id}", json=request_json)
    assert response.status_code == status_code

    if status_code == 200:
        room_response = await ac.get(f"/hotels/{hotel_id}/rooms/{room_id}")
        assert room_response.status_code == 200
        updated_room_data = room_response.json()

        if response_json:
            for key, value in response_json.items():
                assert updated_room_data.get(key) == value

    elif response_json:
        assert response.json() == response_json


@pytest.mark.parametrize(
    "hotel_id, room_id, status_code, response_json",
    [
        (3, 4, 200, {"status": "ok"}),
        (999, 4, 404, {"detail": "Hotel not found"}),
        (3, 999, 404, {"detail": "Room not found"}),
        (3, 4, 404, {"detail": "Room not found"}),
        (0, 4, 422, None),
        (3, 0, 422, None),
        (3, 9999999999999, 422, None),
        (9999999999999, 4, 422, None),
    ],
)
async def test_delete_room(
    ac: AsyncClient, hotel_id: int, room_id: int, status_code: int, response_json: dict | None
):
    response = await ac.delete(f"/hotels/{hotel_id}/rooms/{room_id}")

    assert response.status_code == status_code

    if response_json:
        assert response.json() == response_json

    if status_code == 200:
        get_response = await ac.get(f"/hotels/{hotel_id}/rooms/{room_id}")
        assert get_response.status_code == 404
        assert get_response.json() == {"detail": "Room not found"}

    elif response_json:
        assert response.json() == response_json
