from fastapi import APIRouter, Body

from src.exceptions import (
    ObjectNotFoundException,
    NoAvailableRoomsException,
    RoomNotFoundHTTPException,
    NoAvailableRoomsHTTPException,
)
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.api.dependencies import DBDep, UserIdDep


router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("")
async def create_booking(
    db: DBDep,
    user_id: UserIdDep,
    booking_data: BookingAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Room 10",
                "description": "July 4th - July 11th",
                "value": {
                    "room_id": 10,
                    "date_from": "2025-07-04",
                    "date_to": "2025-07-11",
                },
            },
            "2": {
                "summary": "Room 10",
                "description": "July 15th - July 22th",
                "value": {
                    "room_id": 10,
                    "date_from": "2025-07-15",
                    "date_to": "2025-07-22",
                },
            },
            "3": {
                "summary": "Room 11",
                "description": "July 4th - July 9th",
                "value": {
                    "room_id": 11,
                    "date_from": "2025-07-04",
                    "date_to": "2025-07-09",
                },
            },
            "4": {
                "summary": "Room 11",
                "description": "Aug 4th - Aug 11th",
                "value": {
                    "room_id": 11,
                    "date_from": "2025-08-04",
                    "date_to": "2025-08-11",
                },
            },
        }
    ),
):
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException
    _booking_data = BookingAdd(user_id=user_id, price=room.price, **booking_data.model_dump())
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=room.hotel_id)
    except NoAvailableRoomsException:
        raise NoAvailableRoomsHTTPException

    await db.commit()
    return {"status": "ok", "data": booking}


@router.delete("{booking_id}")
async def delete_booking(db: DBDep, booking_id: int):
    await db.bookings.delete(id=booking_id)
    await db.commit()
    return {"status": "ok"}
