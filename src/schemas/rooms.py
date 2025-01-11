from pydantic import BaseModel

from src.schemas.facilities import Facility


class RoomAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] = []


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] = []


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
