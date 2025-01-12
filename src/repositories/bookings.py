from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.models.bookings import BookingsORM


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingDataMapper
