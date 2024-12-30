from fastapi import Query, APIRouter, Body, HTTPException

from sqlalchemy import insert, select, func, update, delete

from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import session_maker

from src.models.hotels import HotelsORM
from src.database import engine

from repositories.hotels import HotelsRepository

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None),
        location: str | None = Query(None),
):
    async with session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=pagination.per_page,
            offset=pagination.per_page * (pagination.page - 1))


@router.post("")
async def add_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
        "summary": "NY",
        "value": {
            "title": "Grand NY 5 Stars",
            "location": "New York. 12nd Twice street",
        }
    },
    "2": {
            "summary": "Amsterdam",
            "value": {
                "title": "Rainbow Hotel-Club",
                "location": "Amsterdam. 12st and mainfield",
            }
        }
})):
    async with session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": "ok", "data": hotel}


@router.put(
    "/{hotel_id}",
    summary="Edit The Entire Hotel")
async def edit_hotel(
        hotel_id: int,
        hotel_data: Hotel
):
    async with session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
        return {"status": "ok"}


@router.patch(
    "/{hotel_id}",
    summary="Partially Edit Hotel",
    description="""
    <h3>Description</h3>
    You can edit several or all attributes of the hotel.""")
def partially_update_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    pass


@router.delete('/{hotel_id}')
async def delete_hotel(hotel_id: int):
    async with session_maker() as session:
        await HotelsRepository(session).delete(hotel_id)
        await session.commit()
        return {"status": "ok"}