from src.repositories.base import BaseRepository
from src.schemas.bookings import Booking
from src.models.bookings import BookingsORM


class BookingsRepository(BaseRepository):
    model = BookingsORM
    schema = Booking

