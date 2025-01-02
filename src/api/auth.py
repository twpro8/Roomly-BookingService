from fastapi import APIRouter, HTTPException, Response, Request

from sqlalchemy.exc import IntegrityError

from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, AddUser, UserLogin
from src.database import session_maker
from src.services.auth import AuthService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register")
async def register_user(
        data: UserRequestAdd
):
    hashed_password = AuthService().hash_password(data.password)
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

@router.post("/login")
async def login_user(
        data: UserLogin,
        response: Response
):
    async with session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(username=data.username)
        if not user:
            raise HTTPException(status_code=401, detail="User does not exist")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect password")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token, httponly=True)

        return {"status": "ok", "access_token": access_token}
