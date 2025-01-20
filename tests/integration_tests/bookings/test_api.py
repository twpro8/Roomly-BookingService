async def test_add_booking(db, authed_ac):
    room_id = (await db.rooms.get_all())[0].id
    res = await authed_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": "2025-09-02",
            "date_to": "2025-09-12",
        }
    )
    assert res.status_code == 200
    res = res.json()
    assert isinstance(res, dict)
    assert res["status"] == "ok"
    assert "data" in res
