from datetime import date
from typing import Optional

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
        await self.check_hotel_exists(title=data.title, location=data.location)
        new_hotel = await self.db.hotels.add(data)
        await self.db.commit()
        return new_hotel

    async def edit_hotel(self, hotel_id: int, data: HotelAdd) -> None:
        await self.check_hotel_exists(hotel_id=hotel_id, title=data.title, location=data.location)
        await self.db.hotels.edit(data, id=hotel_id)
        await self.db.commit()

    async def partly_edit_hotel(self, hotel_id: int, data: HotelPATCH) -> None:
        await self.check_hotel_exists(hotel_id=hotel_id, title=data.title, location=data.location)
        await self.db.hotels.edit(data, exclude_unset=True, id=hotel_id)
        await self.db.commit()

    async def delete_hotel(self, hotel_id: int) -> None:
        await self.check_hotel_exists(hotel_id=hotel_id)
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

    async def check_hotel_exists(
        self,
        hotel_id: Optional[int] = None,
        location: Optional[str] = None,
        title: Optional[str] = None,
    ) -> None:
        if hotel_id:
            try:
                await self.db.hotels.get_one(id=hotel_id)
            except ObjectNotFoundException:
                raise HotelNotFoundException
        if title and location:
            hotel = await self.db.hotels.get_one_or_none(title=title, location=location)
            if hotel:
                raise HotelAlreadyExistsException
