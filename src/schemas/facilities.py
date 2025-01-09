from pydantic import BaseModel



class FacilityAddRequest(BaseModel):
    title: str


class Facility(FacilityAddRequest):
    id: int
