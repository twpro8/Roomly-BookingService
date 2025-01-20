from datetime import date

from src.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id

    # CREATE
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2025, month=5, day=1),
        date_to=date(year=2025, month=5, day=5),
        price=11,
    )
    new_booking = await db.bookings.add(booking_data)

    # READ
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id
    assert booking.user_id == new_booking.user_id
    assert booking.room_id == new_booking.room_id

    # UPDATE
    update_booking = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2025, month=7, day=7),  # updated
        date_to=date(year=2025, month=8, day=8),  # updated
        price=456,  # updated
    )
    await db.bookings.edit(data=update_booking, id=booking.id)

    updated_booking = await db.bookings.get_one_or_none(id=booking.id)
    assert updated_booking
    assert updated_booking.user_id == booking.user_id
    assert updated_booking.room_id == booking.room_id
    assert updated_booking.date_from != booking.date_from
    assert updated_booking.date_to != booking.date_to
    assert updated_booking.price != booking.price

    # DELETE
    await db.bookings.delete(id=booking.id)
    deleted_booking = await db.bookings.get_one_or_none(id=booking.id)
    assert not deleted_booking
