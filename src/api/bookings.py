from fastapi import APIRouter, Body

from src.schemas.bookings import Booking, BookingAddRequest, BookingAdd
from src.api.dependencies import DBDep, PaginationDep, UserIdDep


router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("")
async def create_booking(
        db: DBDep,
        user_id: UserIdDep,
        booking_data: BookingAddRequest = Body()
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    _booking_data = BookingAdd(user_id=user_id, price=room.price, **booking_data.model_dump())
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "ok", "data": booking}

