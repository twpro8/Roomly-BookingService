from datetime import date
from pydantic import BaseModel, Field, ConfigDict


class BookingAddRequest(BaseModel):
    room_id: int = Field(gt=0, lt=2147483647)
    date_from: date
    date_to: date

    model_config = ConfigDict(extra="forbid")


class BookingAdd(BaseModel):
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int = Field(gt=0, lt=2147483647)


class Booking(BookingAdd):
    id: int
