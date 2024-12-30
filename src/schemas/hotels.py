from pydantic import BaseModel, Field


class Hotel(BaseModel):
    id: int
    title: str
    location: str

class HotelAdd(BaseModel):
    title: str
    location: str

class HotelPATCH(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)
