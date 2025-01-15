import json

from fastapi import APIRouter, Body

from src import redis_manager
from src.schemas.facilities import FacilityAddRequest
from src.api.dependencies import DBDep


router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("")
async def get_facilities(db: DBDep):
    facilities_from_cache = await redis_manager.get("facilities")
    if not facilities_from_cache:
        facilities = await db.facilities.get_all()
        facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
        facilities_json = json.dumps(facilities_schemas)
        await redis_manager.set("facilities", facilities_json, 5)

        return facilities
    else:
        facilities_dicts = json.loads(facilities_from_cache)
        return facilities_dicts

@router.post("")
async def add_facility(
        db: DBDep,
        facility: FacilityAddRequest = Body()
):
    res = await db.facilities.add(facility)
    await db.commit()
    return {"status": "ok", "facility": res}

