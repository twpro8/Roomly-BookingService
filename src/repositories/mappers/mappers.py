from src.models.hotels import HotelsORM
from src.repositories.mappers.base import DataMapper
from src.schemas.hotels import Hotel


class HotelDataMapper(DataMapper):
    db_model = HotelsORM
    schema = Hotel
