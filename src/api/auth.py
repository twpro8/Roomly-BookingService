
from fastapi import APIRouter

from repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, AddUser
from src.api.dependencies import PaginationDep
from src.database import session_maker


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register")
async def register_user(
        data: UserRequestAdd
):
    hashed_password = ...
    new_user_data = AddUser(username=data.username, email=data.email, hashed_password=hashed_password)
    async with session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()