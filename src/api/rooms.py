from fastapi import APIRouter, Body

from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest
from src.api.dependencies import DBDep


router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(db: DBDep, hotel_id: int):
    return await db.rooms.get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room_by_id(db: DBDep, hotel_id: int, room_id: int):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms/")
async def add_room(db: DBDep, hotel_id: int, room_data: RoomAddRequest = Body(openapi_examples={
    "1": {
        "summary": "Ex1",
        "value": {
            "title": "No V.I.P.",
            "description": "For best people",
            "price": 1200,
            "quantity": 4
        }
    },
    "2": {
        "summary": "Ex2",
        "value": {
            "title": "V.I.P.",
            "price": 1200,
            "quantity": 4
        }
    }
})):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    await db.commit()
    return {"status": "ok", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}",
            summary="Edit The Entire Room",
            description="""
                <h3>Description</h3>
                You have to edit all the attributes of the room at once""")
async def edit_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomAddRequest
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(room_data, id=room_id)
    await db.commit()
    return {"status": "ok"}


@router.patch("/{hotel_id}/rooms/{room_id}",
            summary="Partially Edit Room",
            description="""
            <h3>Description</h3>
            You can edit several or all the attributes of the room""")
async def partially_edit_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "ok"}


@router.delete("/{hotel_id}/rooms/{room_id}",
   summary='Delete Room',
   description='<h3>Permanently delete room by id</h3>')
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
        await db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await db.commit()
        return {"status": "ok"}

