from pydantic import BaseModel, Field, model_validator, ConfigDict


class HotelAdd(BaseModel):
    title: str = Field(min_length=5, max_length=100)
    location: str = Field(min_length=5, max_length=100)

    model_config = ConfigDict(extra="forbid")


class HotelPATCH(BaseModel):
    title: str | None = Field(None, min_length=5, max_length=100)
    location: str | None = Field(None, min_length=5, max_length=100)

    @model_validator(mode="before")
    def check_at_least_one_field(cls, values):
        title = values.get("title")
        location = values.get("location")

        if not title and not location:
            raise ValueError("At least one of title or location must be provided")

        return values

    model_config = ConfigDict(extra="forbid")


class Hotel(HotelAdd):
    id: int = Field(gt=0, lt=2147483647)
