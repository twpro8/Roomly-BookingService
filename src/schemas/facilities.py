from pydantic import BaseModel, ConfigDict, Field


class FacilityAddRequest(BaseModel):
    title: str = Field(min_length=2, max_length=100)

    model_config = ConfigDict(extra="forbid")


class Facility(FacilityAddRequest):
    id: int


class RoomFacilityAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomFacility(RoomFacilityAdd):
    id: int
