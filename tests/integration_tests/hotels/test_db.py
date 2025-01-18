from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager
from src.database import null_pool_session_maker


async def test_add_hotel():
    hotel_data = HotelAdd(title="Pride", location="Amsterdam")
    async with DBManager(session_factory=null_pool_session_maker) as db:
        new_hotel_data = await db.hotels.add(hotel_data)
        print(f"{new_hotel_data=}")
