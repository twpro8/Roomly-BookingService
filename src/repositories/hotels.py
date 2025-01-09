from datetime import date

from sqlalchemy import select, func

from src.repositories.base import BaseRepository
from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.schemas.hotels import Hotel

from src.repositories.utils import rooms_ids_for_booking


class HotelsRepository(BaseRepository):
    model = HotelsORM
    schema = Hotel

    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            location,
            title,
            limit,
            offset
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)

        get_hotel_ids = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
        )

        get_hotel_ids = (
            get_hotel_ids
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
        )

        query = (
            select(HotelsORM).select_from(HotelsORM)
        )

        if title:
            query = (
                query
                .filter(func.lower(HotelsORM.title)
                .contains(title.strip().lower()))
            )
        if location:
            query = (
                query
                .filter(func.lower(HotelsORM.location)
                .contains(location.strip().lower())))

        query = (
            query
            .filter(HotelsORM.id.in_(get_hotel_ids))
            .limit(limit)
            .offset(offset)
        )
        res = await self.session.execute(query)

        return [self.schema.model_validate(model, from_attributes=True) for model in res.scalars().all()]

