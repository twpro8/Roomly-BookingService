from datetime import date

from sqlalchemy import select, func

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsORM
from src.models.bookings import BookingsORM
from src.schemas.rooms import Room
from src.database import engine


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date
    ):
        rooms_count = (
            select(BookingsORM.room_id, func.count("*").label("total_booked"))
            .select_from(BookingsORM)
            .filter(BookingsORM.date_from <= date_to,
                    BookingsORM.date_to >= date_from)
            .group_by(BookingsORM.room_id)
            .cte(name="rooms_count")
        )
        rooms_left = (
            select(
                RoomsORM.id.label("room_id"),
                (RoomsORM.quantity - func.coalesce(rooms_count.c.total_booked, 0)).label("rooms_left"))
            .select_from(RoomsORM)
            .outerjoin(rooms_count, RoomsORM.id == rooms_count.c.room_id)
            .cte(name="rooms_left")
        )
        rooms_ids_for_hotel = (
            select(RoomsORM.id)
            .select_from(RoomsORM)
            .filter_by(hotel_id=hotel_id)
            .subquery(name="rooms_ids_for_hotel")
        )
        get_rooms_ids = (
            select(rooms_left.c.room_id)
            .select_from(rooms_left)
            .filter(
                rooms_left.c.rooms_left > 0,
                rooms_left.c.room_id.in_(rooms_ids_for_hotel)
            )
        )
        # print(get_rooms_ids.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        return await self.get_filtered(RoomsORM.id.in_(get_rooms_ids))

