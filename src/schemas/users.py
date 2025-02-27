from pydantic import BaseModel, EmailStr, Field, model_validator, ConfigDict


class UserDTO(BaseModel):
    id: int
    username: str = Field(min_length=4, max_length=20)
    email: EmailStr = Field(max_length=50)
    bio: str | None = Field(default=None, min_length=2, max_length=100)


class UserRequestAddDTO(BaseModel):
    username: str = Field(min_length=5, max_length=20)
    email: EmailStr = Field(max_length=50)
    password: str = Field(min_length=6, max_length=50)

    model_config = ConfigDict(extra="forbid")


class UserAddDTO(BaseModel):
    username: str = Field(min_length=5, max_length=20)
    email: EmailStr = Field(max_length=50)
    hashed_password: str


class UserWithHashedPasswordDTO(UserDTO):
    hashed_password: str


class UserLoginDTO(BaseModel):
    username: str = Field(min_length=5, max_length=20)
    password: str = Field(min_length=6, max_length=50)

    model_config = ConfigDict(extra="forbid")


class UserPatchRequestDTO(BaseModel):
    username: str | None = Field(default=None, min_length=5, max_length=20)
    password: str | None = Field(default=None, min_length=6, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=50)
    bio: str | None = Field(default=None, min_length=2, max_length=100)

    @model_validator(mode="before")
    def check_at_least_one_field(cls, values):
        username = values.get("username")
        password = values.get("password")
        email = values.get("email")
        bio = values.get("bio")

        if not any([username, password, email, bio]):
            raise ValueError("At least one field must be provided")

        return values

    model_config = ConfigDict(extra="forbid")


class UserPatchDTO(BaseModel):
    username: str | None = None
    hashed_password: str | None = None
    email: EmailStr | None = None
    bio: str | None = None
