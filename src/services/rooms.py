from datetime import date

from src.exceptions import (
    check_date_to_after_date_from,
    RoomNotFoundException,
    RoomAlreadyExistsException,
    HotelNotFoundException,
)
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAddRequest, RoomAdd, RoomPatchRequest, RoomPatch
from src.services.base import BaseService


class RoomService(BaseService):
    async def get_rooms(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        check_date_to_after_date_from(date_from, date_to)
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

    async def get_room(self, room_id: int, hotel_id: int):
        return await self.db.rooms.get_one_or_none_with_rels(id=room_id, hotel_id=hotel_id)

    async def creat_room(
        self,
        hotel_id: int,
        room_data: RoomAddRequest,
    ):
        existing_room = await self.db.rooms.get_one_or_none(
            hotel_id=hotel_id, title=room_data.title
        )
        if existing_room:
            raise RoomAlreadyExistsException

        hotel = await self.db.hotels.check_exists(id=hotel_id)
        if not hotel:
            raise HotelNotFoundException

        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        room = await self.db.rooms.add(_room_data)
        rooms_facilities_data = [
            RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids
        ]
        if rooms_facilities_data:
            await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
        await self.db.commit()
        return room

    async def edit_room(self, hotel_id: int, room_id: int, room_data: RoomAddRequest) -> None:
        hotel = await self.db.hotels.check_exists(id=hotel_id)
        if not hotel:
            raise HotelNotFoundException
        room = await self.db.rooms.check_exists(id=room_id, hotel_id=hotel_id)
        if not room:
            raise RoomNotFoundException

        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        await self.db.rooms.edit(_room_data, id=room_id)
        await self.db.rooms_facilities.add_facilities(
            room_id=room_id, facilities_ids=room_data.facilities_ids
        )
        await self.db.commit()

    async def partly_edit_room(
        self, hotel_id: int, room_id: int, room_data: RoomPatchRequest
    ) -> None:
        hotel = await self.db.hotels.check_exists(id=hotel_id)
        if not hotel:
            raise HotelNotFoundException
        room = await self.db.rooms.check_exists(id=room_id, hotel_id=hotel_id)
        if not room:
            raise RoomNotFoundException

        _model_dump = room_data.model_dump(exclude_unset=True)
        _room_data = RoomPatch(hotel_id=hotel_id, **_model_dump)
        await self.db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        if "facilities_ids" in _model_dump:
            await self.db.rooms_facilities.add_facilities(
                room_id=room_id, facilities_ids=_model_dump.get("facilities_ids")
            )
        await self.db.commit()

    async def delete_room(self, hotel_id: int, room_id: int) -> None:
        hotel = await self.db.hotels.check_exists(id=hotel_id)
        if not hotel:
            raise HotelNotFoundException
        room = await self.db.rooms.check_exists(id=room_id, hotel_id=hotel_id)
        if not room:
            raise RoomNotFoundException

        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()
