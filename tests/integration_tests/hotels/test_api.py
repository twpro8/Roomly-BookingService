from typing import Any

import pytest
from src.schemas.hotels import Hotel


async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels",
        params={
            "date_from": "2025-09-02",
            "date_to": "2025-09-12",
        },
    )
    hotel_list = response.json()

    assert response.status_code == 200
    assert isinstance(hotel_list, list)


@pytest.mark.parametrize("hotel_id", [1, 2, 3])
async def test_get_hotel(ac, hotel_id: int):
    response = await ac.get(f"/hotels/{hotel_id}")
    hotel = response.json()

    assert response.status_code == 200
    assert isinstance(hotel, dict)
    validate_hotel_data(hotel, hotel_id, hotel.get("title"), hotel.get("location"))


@pytest.mark.parametrize(
    "title, location, status_code, surprise",
    [
        # Test case 1: Valid hotel data
        ("GoodPlace1", "Amsterdam", 200, None),
        ("GoodPlace10", "Amsterdam0", 200, None),
        ("GoodPlace11", "Amsterdam9", 200, None),
        ("GoodPlace12", "Amsterdam8", 200, None),
        ("GoodPlace13", "Amsterdam7", 200, None),
        ("GoodPlace14", "Amsterdam6", 200, None),
        ("GoodPlace15", "Amsterdam5", 200, None),
        ("GoodPlace16", "Amsterdam4", 200, None),
        ("GoodPlace17", "Amsterdam3", 200, None),
        ("GoodPlace18", "Amsterdam2", 200, None),
        # Test case 2: Valid hotel data
        ("GoodPlace2", "New York", 200, None),
        # Test case 3: Valid hotel data
        ("GoodPlace3", "Somewhere Else", 200, None),
        # Test case 4: Empty title
        ("", "Amsterdam", 422, None),
        # Test case 5: Empty location, should return 422
        ("GoodPlace", "", 422, None),
        # Test case 6: Max length for title
        ("A" * 100, "ValidLocation", 200, None),
        # Test case 7: Exceeded max length for title
        ("A" * 101, "ValidLocation", 422, None),
        # Test case 8: Max length for location
        ("ValidName", "B" * 100, 200, None),
        # Test case 9: Exceeded max length for location
        ("ValidName", "B" * 101, 422, None),
        # Test case 10 Duplicate hotel
        ("GoodPlace1", "Amsterdam", 409, None),
        # Test case 11: Unexpected additional field
        ("GoodPlace", "Amsterdam", 422, "Boooo!"),
        # Test case 12: Unexpected additional field
        ("GoodPlace", "Amsterdam", 422, 11111),
        # Test case 13: Duplicate hotel
        ("UniquePlace", "Amsterdam", 200, None),
    ],
)
async def test_add_hotel(
    ac, title: str, location: str, status_code: int | None, surprise: Any | None
):
    request_json = {"title": title, "location": location}
    if surprise is not None:
        request_json["surprise"] = surprise

    response = await ac.post("/hotels", json=request_json)
    assert response.status_code == status_code

    if response.status_code == 200:
        assert "data" in response.json()
        hotel = response.json().get("data")
        assert response.json()["status"] == "ok"
        validate_hotel_data(hotel, hotel["id"], title, location)


@pytest.mark.parametrize(
    "hotel_id, new_title, new_location, status_code, surprise",
    [
        # Test case 1: Valid hotel data
        (1, "New Title 1", "New Location 1", 200, None),
        # Test case 2 Duplicate hotel
        (2, "New Title 1", "New Location 1", 409, None),
        # Test case 3: Unexpected additional field
        (3, "New Title 4", "New Location 4", 422, "Boooo!"),
        # Test case 4: Max length for title
        (1, "1" * 100, "ValidLocation", 200, None),
        # Test case 5: Exceeded max length for title
        (2, "2" * 101, "ValidLocation", 422, None),
        # Test case 6: Max length for location
        (3, "NewValidName", "3" * 100, 200, None),
        # Test case 7: Exceeded max length for location
        (1, "NewValidName", "4" * 101, 422, None),
        # Test case 8: Invalid hotel id
        (-1, "New Title 5", "New Location 5", 422, None),
        # Test case 9: Hotel not found
        (1024, "New grate Title", "One More New Location", 404, None),
        # Test case 10: Missing all
        (None, None, None, 422, None),
        # Test case 11: Missing title
        (2, "", "Somewhere else.. New", 422, None),
        # Test case 12: Missing all
        (3, "", "", 422, None),
        # Test case 13: Missing location
        (1, "New is New", "", 422, None),
        # Test case 14: Invalid location
        (2, "Title is New", 1, 422, None),
    ],
)
async def test_edit_hotel(
    ac,
    db,
    hotel_id: int,
    new_title: str,
    new_location: str,
    status_code: int,
    surprise: Any | None,
):
    request_json = {"title": new_title, "location": new_location}
    if surprise is not None:
        request_json["surprise"] = surprise

    response = await ac.put(f"/hotels/{hotel_id}", json=request_json)
    assert response.status_code == status_code

    if response.status_code == 200:
        assert response.json()["status"] == "ok"
        edited_hotel = (await ac.get(f"/hotels/{hotel_id}")).json()
        validate_hotel_data(edited_hotel, hotel_id, new_title, new_location)
        assert edited_hotel["title"] == new_title
        assert edited_hotel["location"] == new_location


@pytest.mark.parametrize(
    "hotel_id, new_title, new_location, status_code, surprise",
    [
        # Test case 1: Valid hotel data
        (4, "New Title 1", "New Location 1", 200, None),
        # Test case 2: Duplicate hotel
        (5, "New Title 1", "New Location 1", 409, None),
        # Test case 3: Unexpected additional field
        (6, "New Title 4", "New Location 4", 422, "Boooo!"),
        # Test case 4: Exceeded max length for title
        (4, "1" * 100, "ValidLocation1", 200, None),
        # Test case 5: Exceeded max length for title
        (5, "2" * 101, "ValidLocation1", 422, None),
        # Test case 6: Max length for location
        (6, "NewValidName1", "3" * 100, 200, None),
        # Test case 7: Exceeded max length for location
        (4, "NewValidName1", "4" * 101, 422, None),
        # Test case 8: Invalid hotel id
        (-1, "New Title 5", "New Location 5", 422, None),
        # Test case 9: Hotel not found
        (1024, "New grate Title", "One More New Location", 404, None),
        # Test case 10: Empty title
        (5, "", "Somewhere else.. New", 422, None),
        (5, None, "Somewhere else.. New", 200, None),
        # Test case 11: Empty title and location
        (6, "", "", 422, None),
        # Test case 12: Empty location
        (4, "New is New", "", 422, None),
        (4, "New is New", None, 200, None),
        # Test case 13: Invalid location (numeric)
        (5, "Title is New", 1, 422, None),
        # Test case 14: Missing all
        (None, None, None, 422, None),
    ],
)
async def test_partly_edit_hotel(
    ac,
    hotel_id: int,
    new_title: str | None,
    new_location: str | None,
    status_code: int | None,
    surprise: Any | None,
):
    old_hotel = (await ac.get(f"/hotels/{hotel_id}")).json()

    update_data = {}
    if new_title is not None:
        update_data["title"] = new_title
    if new_location is not None:
        update_data["location"] = new_location
    if surprise is not None:
        update_data["surprise"] = surprise

    response = await ac.patch(f"/hotels/{hotel_id}", json=update_data)
    assert response.status_code == status_code

    if response.status_code == 200:
        assert response.json()["status"] == "ok"

        edited_hotel = (await ac.get(f"/hotels/{hotel_id}")).json()
        validate_hotel_data(
            edited_hotel,
            hotel_id,
            new_title or old_hotel["title"],
            new_location or old_hotel["location"],
        )


@pytest.mark.parametrize(
    "hotel_id, status_code",
    [
        (7, 200),
        (111, 404),
        (8, 200),
        (-1, 422),
        (0, 422),
        (9, 200),
        (99999999999, 422),
        (None, 422),
    ],
)
async def test_delete_hotel(ac, hotel_id: int, status_code: int):
    response = await ac.delete(f"/hotels/{hotel_id}")
    assert response.status_code == status_code
    if response.status_code == 200:
        is_deleted = await ac.get(f"/hotels/{hotel_id}")
        assert is_deleted.status_code == 404


def validate_hotel_data(hotel, hotel_id: int, title: str | None, location: str | None):
    assert Hotel.model_validate(hotel)
    assert hotel["id"] == hotel_id
    if title is not None:
        assert hotel["title"] == title
    if location is not None:
        assert hotel["location"] == location
