from pydantic import BaseModel, ConfigDict, Field


class FacilityAddRequestDTO(BaseModel):
    title: str = Field(min_length=2, max_length=100)

    model_config = ConfigDict(extra="forbid")


class FacilityDTO(FacilityAddRequestDTO):
    id: int


class RoomFacilityAddDTO(BaseModel):
    room_id: int
    facility_id: int


class RoomFacilityDTO(RoomFacilityAddDTO):
    id: int
