from fastapi import APIRouter, Body

from src.api.utils import TypeID
from src.exceptions import (
    NoAvailableRoomsException,
    RoomNotFoundHTTPException,
    NoAvailableRoomsHTTPException,
    RoomNotFoundException,
    BookingNotFoundException,
    BookingNotFoundHTTPException,
    HotelNotFoundException,
    HotelNotFoundHTTPException,
)
from src.schemas.bookings import BookingAddRequestDTO
from src.api.dependencies import DBDep, UserIdDep
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("/me")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    return await BookingService(db).get_my_bookings(user_id)


@router.post("")
async def add_booking(
    db: DBDep,
    user_id: UserIdDep,
    booking_data: BookingAddRequestDTO = Body(),
):
    try:
        booking = await BookingService(db).create_booking(user_id, booking_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except NoAvailableRoomsException:
        raise NoAvailableRoomsHTTPException

    return {"status": "ok", "data": booking}


@router.delete("/{booking_id}")
async def delete_booking(db: DBDep, user_id: UserIdDep, booking_id: TypeID):
    try:
        await BookingService(db).delete_booking(user_id, booking_id)
    except BookingNotFoundException:
        raise BookingNotFoundHTTPException
    return {"status": "ok"}
