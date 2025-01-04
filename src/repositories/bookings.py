from sqlalchemy import insert
from pydantic import BaseModel

from src.repositories.base import BaseRepository
from src.models.bookings import BookingsORM
from src.schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = BookingsORM
    schema = Booking

