from fastapi import APIRouter, Response

from src.api.dependencies import UserIdDep
from src.exceptions import (
    ObjectAlreadyExistsException,
    UserAlreadyExistsHTTPException,
    UserDoesNotExistHTTPException,
    IncorrectPasswordHTTPException,
)
from src.schemas.users import UserRequestAdd, AddUser, UserLogin
from src.services.auth import AuthService

from src.api.dependencies import DBDep


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register")
async def register_user(db: DBDep, data: UserRequestAdd):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = AddUser(
        username=data.username, email=data.email, hashed_password=hashed_password
    )
    try:
        await db.users.add(new_user_data)
    except ObjectAlreadyExistsException:
        raise UserAlreadyExistsHTTPException

    await db.commit()

    return {"status": "ok"}


@router.post("/login")
async def login_user(db: DBDep, data: UserLogin, response: Response):
    user = await db.users.get_user_with_hashed_password(username=data.username)
    if not user:
        raise UserDoesNotExistHTTPException
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise IncorrectPasswordHTTPException
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token, httponly=True)

    return {"status": "ok", "access_token": access_token}


@router.get("/profile")
async def get_me(db: DBDep, user_id: UserIdDep):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "ok"}
