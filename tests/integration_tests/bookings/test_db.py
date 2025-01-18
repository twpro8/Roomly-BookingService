from datetime import date

from src.schemas.bookings import BookingAdd


async def test_add_booking(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2025, month=5, day=1),
        date_to=date(year=2025, month=5, day=5),
        price=11
    )
    await db.bookings.add(booking_data)
    await db.commit()
