from datetime import date

from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache

from src.exceptions import (
    ObjectNotFoundException,
    HotelNotFoundHTTPException,
)
from src.schemas.hotels import HotelPATCH, HotelAdd
from src.api.dependencies import PaginationDep, DBDep
from src.services.hotels import HotelService

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
    hotels = await HotelService(db).get_hotels(
        pagination,
        title,
        location,
        date_from,
        date_to,
    )
    return hotels



@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        hotel = await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
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
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"status": "ok", "data": hotel}


@router.put("/{hotel_id}", summary="Edit The Entire Hotel")
async def edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await HotelService(db).edit_hotel(hotel_id, hotel_data)
    return {"status": "ok"}


@router.patch(
    "/{hotel_id}",
    summary="Partially Edit Hotel",
    description="""
    <h3>Description</h3>
    You can edit several or all attributes of the hotel.""",
)
async def partly_edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPATCH):
    await HotelService(db).partly_edit_hotel(hotel_id, hotel_data)
    return {"status": "ok"}


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "ok"}
