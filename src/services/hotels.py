from datetime import date

from src.api.dependencies import PaginationDep
from src.exceptions import (
    check_date_to_after_date_from,
    ObjectNotFoundException,
    HotelNotFoundException,
    HotelAlreadyExistsException,
)
from src.schemas.hotels import HotelAdd, HotelPATCH
from src.services.base import BaseService


class HotelService(BaseService):
    async def get_hotels(
        self,
        pagination: PaginationDep,
        title: str | None,
        location: str | None,
        date_from: date,
        date_to: date,
    ):
        check_date_to_after_date_from(date_from, date_to)
        hotels = await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=pagination.per_page,
            offset=pagination.per_page * (pagination.page - 1),
        )
        return hotels

    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def add_hotel(self, data: HotelAdd):
        hotel = await self.db.hotels.get_one_or_none(location=data.location)
        if hotel:
            raise HotelAlreadyExistsException

        new_hotel = await self.db.hotels.add(data)
        await self.db.commit()
        return new_hotel

    async def edit_hotel(self, hotel_id: int, data: HotelAdd) -> None:
        await self.db.hotels.edit(data, id=hotel_id)
        await self.db.commit()

    async def partly_edit_hotel(self, hotel_id: int, data: HotelPATCH) -> None:
        await self.db.hotels.edit(data, exclude_unset=True, id=hotel_id)
        await self.db.commit()

    async def delete_hotel(self, hotel_id: int) -> None:
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

    async def get_hotel_with_check(self, hotel_id: int):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
