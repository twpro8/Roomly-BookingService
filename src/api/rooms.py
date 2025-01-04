from fastapi import APIRouter, Body

from src.schemas.rooms import RoomAdd, RoomPATCH, RoomPut
from src.database import session_maker

from src.repositories.rooms import RoomsRepository


router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get("/{hotel_id}/rooms")
async def get_rooms():
    async with session_maker() as session:
        return await RoomsRepository(session).get_all()

@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room_by_id(room_id: int):
    async with session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id)

@router.post("/{hotel_id}/rooms/")
async def add_room(room_data: RoomAdd = Body(openapi_examples={
    "1": {
        "summary": "Ex1",
        "value": {
            "id_hotel": 48,
            "title": "No V.I.P.",
            "description": "For best people",
            "price": 1200,
            "quantity": 4
        }
    },
    "2": {
        "summary": "Ex2",
        "value": {
            "id_hotel": 48,
            "title": "V.I.P.",
            "price": 1200,
            "quantity": 4
        }
    }
})):
    async with session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {"status": "ok", "data": room}

@router.put("/{hotel_id}/rooms/{room_id}",
            summary="Edit The Entire Room",
            description="""
                <h3>Description</h3>
                You have to edit all the attributes of the room at once""")
async def edit_room(
        room_id: int,
        room_data: RoomPut
):
    async with session_maker() as session:
        await RoomsRepository(session).edit(room_data, id=room_id)
        await session.commit()
        return {"status": "ok"}

@router.patch("/{hotel_id}/rooms/{room_id}",
            summary="Partially Edit Room",
            description="""
            <h3>Description</h3>
            You can edit several or all the attributes of the room""")
async def partially_edit_room(
        room_id: int,
        room_data: RoomPATCH
):
    async with session_maker() as session:
        await RoomsRepository(session).edit(room_data, exclude_unset=True, id=room_id)
        await session.commit()
        return {"status": "ok"}

@router.delete("/{hotel_id}/rooms/{room_id}",
   summary='Delete Room',
   description='<h3>Permanently delete room by id</h3>')
async def delete_room(room_id: int):
    async with session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
        return {"status": "ok"}
