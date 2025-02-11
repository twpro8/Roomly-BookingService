from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: int
    username: str = Field(min_length=4, max_length=20)
    email: EmailStr = Field(max_length=50)
    bio: str | None = Field(default=None, max_length=200)


class UserRequestAdd(BaseModel):
    username: str = Field(min_length=5, max_length=20)
    email: EmailStr = Field(max_length=50)
    password: str = Field(min_length=6, max_length=50)

    class Config:
        extra = "forbid"


class AddUser(BaseModel):
    username: str = Field(min_length=5, max_length=20)
    email: EmailStr = Field(max_length=50)
    hashed_password: str


class UserWithHashedPassword(User):
    hashed_password: str


class UserLogin(BaseModel):
    username: str = Field(min_length=5, max_length=20)
    password: str = Field(min_length=6, max_length=50)

    class Config:
        extra = "forbid"
