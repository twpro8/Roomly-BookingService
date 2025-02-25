from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.exceptions import (
    FacilityNotFoundException,
    FacilityNotFoundHTTPException,
    FacilityAlreadyExistsException,
    FacilityAlreadyExistsHTTPException,
)
from src.schemas.facilities import FacilityAddRequestDTO
from src.api.dependencies import DBDep
from src.services.facilities import FacilityService
from src.api.utils import TypeID


router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("")
@cache(expire=15)
async def get_facilities(db: DBDep):
    return await FacilityService(db).get_facilities()


@router.post("")
async def add_facility(db: DBDep, facility_data: FacilityAddRequestDTO = Body()):
    try:
        facility = await FacilityService(db).add_facility(facility_data)
    except FacilityAlreadyExistsException:
        raise FacilityAlreadyExistsHTTPException
    return {"status": "ok", "data": facility}


@router.delete("/{facility_id}")
async def delete_facility(db: DBDep, facility_id: TypeID):
    try:
        await FacilityService(db).delete_facility(facility_id)
    except FacilityNotFoundException:
        raise FacilityNotFoundHTTPException
    return {"status": "ok"}
