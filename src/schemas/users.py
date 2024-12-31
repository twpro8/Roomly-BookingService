
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    bio: str | None

class UserRequestAdd(BaseModel):
    username: str
    email: EmailStr
    password: str

class AddUser(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
