from pydantic import BaseModel


class FacilityAddRequest(BaseModel):
    title: str


class Facility(FacilityAddRequest):
    id: int


class RoomFacilityAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomFacility(RoomFacilityAdd):
    id: int
