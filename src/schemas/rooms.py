from pydantic import BaseModel, Field


class RoomPut(BaseModel):
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int

class RoomAdd(RoomPut):
    hotel_id: int

class RoomPATCH(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)

class Room(RoomAdd):
    id: int
