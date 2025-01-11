from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsORM
from src.schemas.rooms import Room, RoomWithRels

from src.repositories.utils import rooms_ids_for_booking


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date
    ):
        get_rooms_ids = rooms_ids_for_booking(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

        query = (
            select(self.model)
            .options(selectinload(RoomsORM.facilities))
            .filter(RoomsORM.id.in_(get_rooms_ids))
        )
        res = await self.session.execute(query)
        return [RoomWithRels.model_validate(model, from_attributes=True) for model in res.scalars().all()]
