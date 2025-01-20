from datetime import date

from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.models.bookings import BookingsORM
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import BookingAdd


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingDataMapper

    async def get_checkin_day(self):
        query = (
            select(self.model)
            .where(self.model.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, data: BookingAdd, hotel_id: int):
        rooms_ids_to_get = rooms_ids_for_booking(
            hotel_id=hotel_id,
            date_from=data.date_from,
            date_to=data.date_to
        )
        res = await self.session.execute(rooms_ids_to_get)
        rooms_ids_to_book = res.scalars().all()

        if data.room_id in rooms_ids_to_book:
            booking = await self.add(data)
            return BookingDataMapper.map_to_domain_entity(booking)
        else:
            raise Exception("There is no rooms left")
