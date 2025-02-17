from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.schemas.facilities import FacilityAddRequest
from src.api.dependencies import DBDep
from src.services.facilities import FacilityService
from src.api.utils import TypeID


router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("")
@cache(expire=15)
async def get_facilities(db: DBDep):
    return await FacilityService(db).get_facilities()


@router.post("")
async def add_facility(db: DBDep, facility_data: FacilityAddRequest = Body()):
    facility = await FacilityService(db).add_facility(facility_data)
    return {"status": "ok", "data": facility}


@router.delete("/{facility_id}")
async def delete_facility(db: DBDep, facility_id: TypeID):
    await FacilityService(db).delete_facility(facility_id)
    return {"status": "ok"}
