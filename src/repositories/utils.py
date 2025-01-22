from datetime import date

from sqlalchemy import select, func

from src.models.rooms import RoomsORM
from src.models.bookings import BookingsORM


def rooms_ids_for_booking(date_from: date, date_to: date, hotel_id: int | None = None):
    rooms_count = (
        select(BookingsORM.room_id, func.count("*").label("total_booked"))
        .select_from(BookingsORM)
        .filter(BookingsORM.date_from <= date_to, BookingsORM.date_to >= date_from)
        .group_by(BookingsORM.room_id)
        .cte(name="rooms_count")
    )
    rooms_left = (
        select(
            RoomsORM.id.label("room_id"),
            (RoomsORM.quantity - func.coalesce(rooms_count.c.total_booked, 0)).label("rooms_left"),
        )
        .select_from(RoomsORM)
        .outerjoin(rooms_count, RoomsORM.id == rooms_count.c.room_id)
        .cte(name="rooms_left")
    )

    rooms_ids_for_hotel = select(RoomsORM.id).select_from(RoomsORM)
    if hotel_id is not None:
        rooms_ids_for_hotel = rooms_ids_for_hotel.filter_by(hotel_id=hotel_id)
    rooms_ids_for_hotel = rooms_ids_for_hotel.subquery(name="rooms_ids_for_hotel")

    get_rooms_ids = (
        select(rooms_left.c.room_id)
        .select_from(rooms_left)
        .filter(
            rooms_left.c.rooms_left > 0,
            rooms_left.c.room_id.in_(rooms_ids_for_hotel.select()),
        )
    )
    return get_rooms_ids
