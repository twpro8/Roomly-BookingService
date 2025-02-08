from pydantic import BaseModel, Field

from src.schemas.facilities import Facility


class RoomAddRequest(BaseModel):
    title: str = Field(min_length=5, max_length=50)
    description: str | None = Field(default=None, min_length=5, max_length=50)
    price: int = Field(default=888, gt=0, lt=1000000)
    quantity: int = Field(default=1, gt=0, lt=1000)
    facilities_ids: list[int] = []

    class Config:
        extra = "forbid"


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomPatchRequest(BaseModel):
    title: str | None = Field(default=None, min_length=5, max_length=50)
    description: str | None = Field(default=None, min_length=5, max_length=50)
    price: int | None = Field(default=None, gt=0, lt=1000000)
    quantity: int | None = Field(default=None, gt=0, lt=1000)
    facilities_ids: list[int] = []

    class Config:
        extra = "forbid"


class RoomPatch(BaseModel):
    hotel_id: int
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None


class Room(RoomAdd):
    id: int


class RoomWithRels(Room):
    facilities: list[Facility]
