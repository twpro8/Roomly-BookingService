from datetime import date

from fastapi import Query, APIRouter, Body, HTTPException
from fastapi_cache.decorator import cache

from src.exceptions import ObjectNotFoundException
from src.schemas.hotels import HotelPATCH, HotelAdd
from src.api.dependencies import PaginationDep, DBDep


router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("")
@cache(expire=15)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None),
    location: str | None = Query(None),
    date_from: date = Query(example="2025-07-01"),
    date_to: date = Query(example="2025-07-07"),
):
    if date_to <= date_from:
        raise HTTPException(
            status_code=422,
            detail="Check-out date must be later than the check-in date.",
        )
    hotels = await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=pagination.per_page,
        offset=pagination.per_page * (pagination.page - 1),
    )
    return hotels


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        hotel = await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotel


@router.post("")
async def add_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "NY",
                "value": {
                    "title": "Grand NY 5 Stars",
                    "location": "New York. 12nd Twice street",
                },
            },
            "2": {
                "summary": "Amsterdam",
                "value": {
                    "title": "Rainbow Hotel-Club",
                    "location": "Amsterdam. 12st and mainfield",
                },
            },
        }
    ),
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "ok", "data": hotel}


@router.put("/{hotel_id}", summary="Edit The Entire Hotel")
async def edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "ok"}


@router.patch(
    "/{hotel_id}",
    summary="Partially Edit Hotel",
    description="""
    <h3>Description</h3>
    You can edit several or all attributes of the hotel.""",
)
async def partially_update_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPATCH):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "ok"}


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "ok"}
