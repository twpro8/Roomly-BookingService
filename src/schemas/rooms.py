from pydantic import BaseModel


class RoomAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int

class RoomAdd(RoomAddRequest):
    hotel_id: int

class RoomPut(RoomAddRequest):
    pass

class RoomPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None

class Room(RoomAdd):
    id: int
