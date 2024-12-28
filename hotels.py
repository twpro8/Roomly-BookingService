from fastapi import Query, APIRouter
from schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix="/hotels", tags=["Hotels"])


hotels = [
    {'id': 1, 'title': 'Ivory Coast Inn', 'name': 'emerald_bay'},
    {'id': 2, 'title': 'Crimson Peak Lodge', 'name': 'ivory_coast'},
    {'id': 3, 'title': 'Starlight Inn', 'name': 'blue_horizon'},
    {'id': 4, 'title': 'Golden Palm Retreat', 'name': 'emerald_bay'},
    {'id': 5, 'title': 'Emerald Bay Hotel', 'name': 'crimson_peak'},
    {'id': 6, 'title': 'Amber Waves Lodge', 'name': 'azure_heights'},
    {'id': 7, 'title': 'Amber Waves Lodge', 'name': 'ivory_coast'},
    {'id': 8, 'title': 'Crimson Peak Lodge', 'name': 'starlight_inn'},
    {'id': 9, 'title': 'Azure Heights Resort', 'name': 'ivory_coast'},
    {'id': 10, 'title': 'Moonlight Haven', 'name': 'moonlight_haven'},
    {'id': 11, 'title': 'Silver Springs Resort', 'name': 'moonlight_haven'},
    {'id': 12, 'title': 'Amber Waves Lodge', 'name': 'starlight_inn'},
    {'id': 13, 'title': 'Moonlight Haven', 'name': 'emerald_bay'},
    {'id': 14, 'title': 'Silver Springs Resort', 'name': 'starlight_inn'},
    {'id': 15, 'title': 'Azure Heights Resort', 'name': 'ivory_coast'},
    {'id': 16, 'title': 'Azure Heights Resort', 'name': 'amber_waves'},
    {'id': 17, 'title': 'Golden Palm Retreat', 'name': 'blue_horizon'},
    {'id': 18, 'title': 'Ivory Coast Inn', 'name': 'silver_springs'},
    {'id': 19, 'title': 'Moonlight Haven', 'name': 'amber_waves'},
    {'id': 20, 'title': 'Crimson Peak Lodge', 'name': 'moonlight_haven'},
]


@router.get("")
def get_hotels(
        id: int | None = Query(None, description='Hotel ID'),
        title: str | None = Query(None),
        name: str | None = Query(None),
        page: int | None = Query(None, ge=1),
        per_page: int | None = Query(None, ge=1, le=30),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        if name and hotel['name'] != name:
            continue
        hotels_.append(hotel)
    if page and per_page:
        return hotels_[(page-1) * per_page:(page-1) * per_page + per_page]
    return hotels_


@router.post("")
def create_hotel(hotel_data: Hotel):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })
    return {"status": "ok"}


@router.put(
    "/{hotel_id}",
    summary="Edit The Entire Hotel")
def update_hotel(
        hotel_id: int,
        hotel_data: Hotel
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel['id'] == hotel_id:
        hotel['title'] = hotel_data.title
        hotel['name'] = hotel_data.name
        return {"status": "ok"}
    return {"status": "hotel not found"}


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
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel['title'] = hotel_data.title
    if hotel_data.name:
        hotel['name'] = hotel_data.name
    return {"status": "ok"}


@router.delete('/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {"status": "ok"}