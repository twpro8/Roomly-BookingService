from fastapi import Query, APIRouter, Body

from sqlalchemy import insert, select

from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import session_maker

from src.models.hotels import HotelsORM
from src.database import engine

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None),
        location: str | None = Query(None),
):
    async with session_maker() as session:
        query = select(HotelsORM)
        if title:
            query = query.filter(HotelsORM.title.ilike(f"%{title}%"))
        if location:
            query = query.filter(HotelsORM.location.ilike(f"%{location}%"))
        query = (
            query
            .limit(pagination.per_page)
            .offset(pagination.per_page * (pagination.page - 1))
        )
        res = await session.execute(query)
        hotels = res.scalars().all()
    return hotels


@router.post("")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
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
                "location": "Amsterdam. 12st and mainst",
            }
        }
})):
    async with session_maker() as session:
        add_hotel_stmt = insert(HotelsORM).values(**hotel_data.model_dump())
        # print(add_hotel_stmt.compile(compile_kwargs={"literal_binds": True}))
        print(add_hotel_stmt.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"status": "ok"}


@router.put(
    "/{hotel_id}",
    summary="Edit The Entire Hotel")
def update_hotel(
        hotel_id: int,
        hotel_data: Hotel
):
    pass


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
def delete_hotel(hotel_id: int):
    pass