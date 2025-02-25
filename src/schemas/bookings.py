from datetime import date
from pydantic import BaseModel, Field, ConfigDict


class BookingAddRequestDTO(BaseModel):
    hotel_id: int = Field(gt=0, lt=2147483647)
    room_id: int = Field(gt=0, lt=2147483647)
    date_from: date
    date_to: date

    model_config = ConfigDict(extra="forbid")


class BookingAddDTO(BaseModel):
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int = Field(gt=0, lt=2147483647)


class BookingDTO(BookingAddDTO):
    id: int
