import pytest


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2025-09-01", "2025-09-10", 200),
    (1, "2025-09-02", "2025-09-11", 200),
    (1, "2025-09-03", "2025-09-12", 200),
    (1, "2025-09-04", "2025-09-13", 200),
    (1, "2025-09-05", "2025-09-14", 200),
    (1, "2025-09-06", "2025-09-15", 500),
    (1, "2025-09-07", "2025-09-16", 500),
    (1, "2025-10-01", "2025-10-10", 200),
    (1, "2025-10-02", "2025-10-11", 200),
])
async def test_add_booking(
        room_id, date_from, date_to, status_code,
        db, authed_ac
):
    # room_id = (await db.rooms.get_all())[0].id
    res = await authed_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert res.status_code == status_code
    if status_code == 200:
        res = res.json()
        assert isinstance(res, dict)
        assert res["status"] == "ok"
        assert "data" in res
