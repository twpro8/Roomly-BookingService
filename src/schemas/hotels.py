from pydantic import BaseModel, Field


class HotelAdd(BaseModel):
    title: str = Field(min_length=5, max_length=100)
    location: str = Field(min_length=5, max_length=100)

    class Config:
        extra = "forbid"


class HotelPATCH(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)

    class Config:
        extra = "forbid"


class Hotel(HotelAdd):
    id: int
