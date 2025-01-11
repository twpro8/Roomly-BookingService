from sqlalchemy import select, insert, delete

from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.schemas.facilities import Facility, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility

    async def add_facilities(self, room_id: int, facilities_ids: list[int]):
        get_existed_f_ids = (
            select(RoomsFacilitiesOrm.facility_id)
            .filter_by(room_id=room_id)
        )
        res = await self.session.execute(get_existed_f_ids)

        existed_f_ids = set(res.scalars().all())
        new_f_ids = set(facilities_ids)

        to_add: set[int] = new_f_ids - existed_f_ids
        to_delete: set[int] = existed_f_ids - new_f_ids

        if to_delete:
            delete_query = (
                delete(RoomsFacilitiesOrm)
                .filter(
                    RoomsFacilitiesOrm.room_id == room_id,
                    RoomsFacilitiesOrm.facility_id.in_(to_delete)
                )
            )
            await self.session.execute(delete_query)
        if to_add:
            insert_values = [{"room_id": room_id, "facility_id": f_id} for f_id in to_add]
            insert_query = insert(RoomsFacilitiesOrm).values(insert_values)
            await self.session.execute(insert_query)
