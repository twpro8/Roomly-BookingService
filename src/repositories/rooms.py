from datetime import date

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from src.exceptions import HotelNotFoundException, RoomNotFoundException
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsORM
from src.repositories.mappers.mappers import RoomDataMapper, RoomWithRelsDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.models.hotels import HotelsORM


class RoomsRepository(BaseRepository):
    model = RoomsORM
    mapper = RoomDataMapper

    async def get_filtered_by_time(self, hotel_id, date_from: date, date_to: date):
        rooms_ids_to_get = rooms_ids_for_booking(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

        query = (
            select(self.model)
            .options(selectinload(RoomsORM.facilities))
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
        )
        res = await self.session.execute(query)
        return [RoomWithRelsDataMapper.map_to_domain_entity(model) for model in res.scalars().all()]

    async def get_one_or_none_with_rels(self, **filter_by):
        query = select(self.model).options(selectinload(RoomsORM.facilities)).filter_by(**filter_by)
        res = await self.session.execute(query)
        model = res.scalars().one_or_none()
        if model is None:
            return None
        return RoomWithRelsDataMapper.map_to_domain_entity(model)

    async def check_hotel_and_room_exists(self, hotel_id: int, room_id: int) -> None:
        try:
            hotel_query = select(HotelsORM).filter_by(id=hotel_id)
            hotel_res = await self.session.execute(hotel_query)
            hotel_res.scalar_one()
        except NoResultFound:
            raise HotelNotFoundException

        try:
            room_query = select(RoomsORM).filter_by(id=room_id, hotel_id=hotel_id)
            room_res = await self.session.execute(room_query)
            room_res.scalar_one()
        except NoResultFound:
            raise RoomNotFoundException
