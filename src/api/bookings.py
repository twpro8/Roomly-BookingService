from fastapi import APIRouter, Body, Path

from src.exceptions import (
    NoAvailableRoomsException,
    RoomNotFoundHTTPException,
    NoAvailableRoomsHTTPException,
    RoomNotFoundException,
)
from src.schemas.bookings import BookingAddRequest
from src.api.dependencies import DBDep, UserIdDep
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("")
async def get_bookings(db: DBDep):
    return await BookingService(db).get_bookings()


@router.get("/me")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    return await BookingService(db).get_my_bookings(user_id)


@router.post("")
async def add_booking(
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
        booking = await BookingService(db).create_booking(user_id, booking_data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except NoAvailableRoomsException:
        raise NoAvailableRoomsHTTPException

    return {"status": "ok", "data": booking}


@router.delete("{booking_id}")
async def delete_booking(db: DBDep, booking_id: int = Path(gt=0)):
    await BookingService(db).delete_booking(booking_id)
    return {"status": "ok"}
