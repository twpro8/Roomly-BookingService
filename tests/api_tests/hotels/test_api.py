import pytest
from src.schemas.hotels import Hotel


def validate_hotel_data(hotel, hotel_id: int, title: str | None, location: str | None):
    assert Hotel.model_validate(hotel)
    assert hotel["id"] == hotel_id
    if title is not None:
        assert hotel["title"] == title
    if location is not None:
        assert hotel["location"] == location


async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels",
        params={
            "date_from": "2025-09-02",
            "date_to": "2025-09-12",
        },
    )
    assert response.status_code == 200


@pytest.mark.parametrize("hotel_id", [1, 2, 3])
async def test_get_hotel(ac, hotel_id: int):
    response = await ac.get(f"/hotels/{hotel_id}")
    hotel = response.json()
    assert response.status_code == 200
    assert isinstance(hotel, dict)
    validate_hotel_data(hotel, hotel_id, hotel.get("title"), hotel.get("location"))


@pytest.mark.parametrize(
    "title, location",
    [
        ("Rainbow Hotel-Club", "Amsterdam. 12st and mainfield"),
        ("Grand NY 5 Stars", "New York. 12nd Twice street"),
        ("Some Hotel", "Somewhere"),
    ],
)
async def test_add_hotel(ac, title: str, location: str):
    response = await ac.post("/hotels", json={"title": title, "location": location})
    hotel = response.json().get("data")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "data" in response.json()
    validate_hotel_data(hotel, hotel["id"], title, location)


@pytest.mark.parametrize(
    "hotel_id, new_title, new_location",
    [
        (4, "New Title 1", "New Location 1"),
        (5, "New Title 2", "New Location 2"),
        (6, "New Title 3", "New Location 3"),
    ],
)
async def test_edit_hotel(ac, hotel_id: int, new_title: str, new_location: str):
    response = await ac.put(
        f"/hotels/{hotel_id}", json={"title": new_title, "location": new_location}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    edited_hotel = (await ac.get(f"/hotels/{hotel_id}")).json()
    validate_hotel_data(edited_hotel, hotel_id, new_title, new_location)


@pytest.mark.parametrize(
    "hotel_id, new_title, new_location",
    [
        (4, "Rainbow Hotel-Club", None),
        (5, "Grand NY 5 Stars", None),
        (6, "Some Hotel", None),
        (4, None, "Amsterdam. 12st and mainfield"),
        (5, None, "New York. 12nd Twice street"),
        (6, None, "Somewhere"),
        (4, "Again New Title 1", "Again New Location 1"),
        (5, "Again New Title 2", "Again New Location 2"),
        (6, "Again New Title 3", "Again New Location 3"),
    ],
)
async def test_partly_edit_hotel(
    ac, hotel_id: int, new_title: str | None, new_location: str | None
):
    old_hotel = (await ac.get(f"/hotels/{hotel_id}")).json()

    update_data = {}
    if new_title is not None:
        update_data["title"] = new_title
    if new_location is not None:
        update_data["location"] = new_location

    response = await ac.patch(f"/hotels/{hotel_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

    edited_hotel = (await ac.get(f"/hotels/{hotel_id}")).json()
    validate_hotel_data(
        edited_hotel,
        hotel_id,
        new_title or old_hotel["title"],
        new_location or old_hotel["location"],
    )


@pytest.mark.parametrize("hotel_id", [4, 5, 6])
async def test_delete_hotel(ac, hotel_id: int):
    response = await ac.delete(f"/hotels/{hotel_id}")
    assert response.status_code == 200

    is_deleted = await ac.get(f"/hotels/{hotel_id}")
    assert is_deleted.status_code == 404
