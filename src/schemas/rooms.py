from pydantic import BaseModel, Field, ConfigDict, model_validator

from src.schemas.facilities import Facility


class RoomAddRequest(BaseModel):
    title: str = Field(min_length=5, max_length=50)
    description: str | None = Field(default=None, min_length=5, max_length=50)
    price: int = Field(default=888, gt=0, lt=1000000)
    quantity: int = Field(default=1, gt=0, lt=1000)
    facilities_ids: list[int] = []

    model_config = ConfigDict(extra="forbid")


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

    @model_validator(mode="before")
    def check_at_least_one_field(cls, values):
        title = values.get("title")
        description = values.get("description")
        price = values.get("price")
        quantity = values.get("quantity")
        facilities_ids = values.get("facilities_ids")

        if not any((title, description, price, quantity, facilities_ids)):
            raise ValueError("At least one of title or location must be provided")

        return values

    model_config = ConfigDict(extra="forbid")


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
