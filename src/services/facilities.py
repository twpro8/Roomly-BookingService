from src.exceptions import (
    ObjectNotFoundException,
    FacilityNotFoundException,
    ObjectAlreadyExistsException,
    FacilityAlreadyExistsException,
)
from src.schemas.facilities import FacilityAddRequest
from src.services.base import BaseService
from src.tasks.tasks import test_task


class FacilityService(BaseService):
    async def get_facilities(self):
        return await self.db.facilities.get_all()

    async def add_facility(self, data: FacilityAddRequest):
        try:
            facility = await self.db.facilities.add(data)
        except ObjectAlreadyExistsException:
            raise FacilityAlreadyExistsException
        await self.db.commit()
        test_task.delay()
        return facility

    async def delete_facility(self, facility_id: int) -> None:
        try:
            await self.db.facilities.get_one(id=facility_id)
        except ObjectNotFoundException:
            raise FacilityNotFoundException
        await self.db.facilities.delete(id=facility_id)
        await self.db.commit()
