
from fastapi import APIRouter, HTTPException

from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, AddUser
from src.database import session_maker


router = APIRouter(prefix="/users", tags=["Users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register_user(
        data: UserRequestAdd
):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = AddUser(username=data.username, email=data.email, hashed_password=hashed_password)
    async with session_maker() as session:
        try:
            await UsersRepository(session).add(new_user_data)
        except IntegrityError as e:
            await session.rollback()
            if "username" in str(e.orig):
                raise HTTPException(status_code=400, detail="Username already exists")
            if "email" in str(e.orig):
                raise HTTPException(status_code=400, detail="Email already exists")

        await session.commit()

    return {"status": "ok"}
