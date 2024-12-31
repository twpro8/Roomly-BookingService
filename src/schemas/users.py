
from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    email: str
    bio: str

class UserRequestAdd(BaseModel):
    username: str
    email: str
    password: str

class AddUser(BaseModel):
    username: str
    email: str
    hashed_password: str
