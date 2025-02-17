import pytest
from typing import Any

from httpx import AsyncClient
from pydantic import ValidationError

from src.schemas.facilities import Facility


@pytest.mark.parametrize(
    "title, status_code, unexpected_field",
    [
        ("Test 1", 200, None),
        ("", 422, None),
        (None, 422, None),
        ("a" * 100, 200, None),
        ("b" * 101, 422, None),
        ("Test 2", 422, "unexpected_field"),
        ("Test 3", 200, None),
        ("Test 4", 200, None),
    ],
)
async def test_add_facility(
    ac: AsyncClient, title: str | None, status_code: int, unexpected_field: Any | None
) -> None:
    request_json = {}
    if title is not None:
        request_json["title"] = title
    if unexpected_field is not None:
        request_json["unexpected_field"] = unexpected_field

    response = await ac.post("/facilities", json=request_json)
    assert response.status_code == status_code

    if response.status_code == 200:
        response_json = response.json()
        assert isinstance(response_json, dict)
        assert response_json["status"] == "ok"
        assert "data" in response_json

        facility_id = response_json["data"]["id"]

        get_current_facilities = await ac.get("/facilities")
        assert get_current_facilities.status_code == 200

        current_facilities = get_current_facilities.json()
        added_facility = next((f for f in current_facilities if f["id"] == facility_id), None)

        assert added_facility is not None, f"Facility with id {facility_id} not found"
        assert added_facility["title"] == title, (
            f"Expected title {title}, but got {added_facility['title']}"
        )


async def test_get_facilities(ac: AsyncClient) -> None:
    response = await ac.get("/facilities")
    assert response.status_code == 200
    facilities = response.json()
    assert isinstance(facilities, list)

    for facility in facilities:
        try:
            Facility(**facility)
        except ValidationError as e:
            assert False, f"Facility data validation failed: {e}"


@pytest.mark.parametrize(
    "f_id, status_code",
    [
        (11, 200),
        (12, 200),
        (14, 200),
        (15, 404),
        (0, 422),
        (-5, 422),
        (9999999999, 422),
        (13, 200),
    ]
)
async def test_delete_facility(ac: AsyncClient, f_id: int, status_code: int) -> None:
    response = await ac.delete(f"/facilities/{f_id}")
    assert response.status_code == status_code

    if response.status_code == 200:
        get_current_facilities = await ac.get("/facilities")
        assert get_current_facilities.status_code == 200

        current_facilities = get_current_facilities.json()
        is_deleted = next((f for f in current_facilities if f["id"] == f_id), None)

        assert is_deleted is None, f"Facility with id {f_id} was not deleted or still exists in the list"
