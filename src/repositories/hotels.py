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
            offset,
    ) -> list[Hotel]:
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
        )
        query = select(HotelsORM).filter(HotelsORM.id.in_(hotels_ids_to_get))
        if location:
            query = query.filter(func.lower(HotelsORM.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsORM.title).contains(title.strip().lower()))
        query = (
            query
            .order_by(HotelsORM.id)
            .limit(limit)
            .offset(offset)
        )
        # print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        res = await self.session.execute(query)

        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in res.scalars().all()]

