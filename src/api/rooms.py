from datetime import date

from fastapi import APIRouter, Body, Query

from src.exceptions import (
    RoomNotFoundHTTPException,
    HotelNotFoundHTTPException,
    HotelNotFoundException,
    RoomNotFoundException,
)
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest
from src.api.dependencies import DBDep
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2025-07-01"),
    date_to: date = Query(example="2025-07-07"),
):
    return await RoomService(db).get_rooms(hotel_id, date_from, date_to)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    room = await RoomService(db).get_room(room_id, hotel_id)
    if room is None:
        raise RoomNotFoundHTTPException
    return room


@router.post("/{hotel_id}/rooms")
async def add_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body()):
    try:
        room = await RoomService(db).creat_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "ok", "data": room}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Edit The Entire Room",
    description="""
                <h3>Description</h3>
                You have to edit all the attributes of the room at once""",
)
async def edit_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest):
    try:
        await RoomService(db).edit_room(hotel_id, room_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "ok"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Partially Edit Room",
    description="""
            <h3>Description</h3>
            You can edit several or all the attributes of the room""",
)
async def partly_edit_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest):
    try:
        await RoomService(db).partly_edit_room(hotel_id, room_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "ok"}


@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="Delete Room",
    description="<h3>Permanently delete room by id</h3>",
)
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        await RoomService(db).delete_room(hotel_id, room_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "ok"}
