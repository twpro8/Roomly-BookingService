from pydantic import BaseModel, ConfigDict


class FacilityAddRequest(BaseModel):
    title: str

    model_config = ConfigDict(extra="forbid")


class Facility(FacilityAddRequest):
    id: int


class RoomFacilityAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomFacility(RoomFacilityAdd):
    id: int
