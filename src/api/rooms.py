from datetime import date

from fastapi import APIRouter, Body, Query

from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest
from src.api.dependencies import DBDep


router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        db: DBDep,
        hotel_id: int,
        date_from: date = Query(example="2025-07-01"),
        date_to: date = Query(example="2025-07-07"),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    return await db.rooms.get_one_or_none_with_rels(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
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
    await db.rooms.edit(_room_data, id=room_id)
    await db.rooms_facilities.add_facilities(room_id=room_id, facilities_ids=room_data.facilities_ids)
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
    _model_dump = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_model_dump)
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    if "facilities_ids" in _model_dump:
        await db.rooms_facilities.add_facilities(room_id=room_id, facilities_ids=_model_dump.get("facilities_ids"))
    await db.commit()
    return {"status": "ok"}


@router.delete("/{hotel_id}/rooms/{room_id}",
   summary='Delete Room',
   description='<h3>Permanently delete room by id</h3>')
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
        await db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await db.commit()
        return {"status": "ok"}
