
from fastapi import APIRouter, Body

from src.schemas.facilities import FacilityAddRequest
from src.api.dependencies import DBDep


router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("")
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()

@router.post("")
async def add_facility(
        db: DBDep,
        facility: FacilityAddRequest = Body()
):
    res = await db.facilities.add(facility)
    await db.commit()
    return {"status": "ok", "facility": res}

