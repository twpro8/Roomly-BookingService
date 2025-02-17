from typing import Any

import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "title, status_code, unexpected_field",
    [
        ("My Facility Title", 200, None),
        ("", 422, None),
        ("a" * 100, 200, None),
        ("b" * 101, 422, None),
        ("My Facility Title 2", 422, "unexpected_field"),
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
        check_exists = await ac.get("/facilities")
        assert check_exists.status_code == 200

        existing_facilities = check_exists.json()
        added_facility = next((f for f in existing_facilities if f["id"] == facility_id), None)

        assert added_facility is not None, f"Facility with id {facility_id} not found"
        assert added_facility["title"] == title, (
            f"Expected title {title}, but got {added_facility['title']}"
        )
