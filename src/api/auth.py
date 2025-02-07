from fastapi import APIRouter, Response

from src.api.dependencies import UserIdDep
from src.exceptions import (
    UserAlreadyExistsHTTPException,
    UserDoesNotExistHTTPException,
    IncorrectPasswordHTTPException,
    UserAlreadyExistsException,
    UserDoesNotExistException,
    IncorrectPasswordException,
)
from src.schemas.users import UserRequestAdd, UserLogin
from src.services.auth import AuthService

from src.api.dependencies import DBDep


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register")
async def register(db: DBDep, data: UserRequestAdd):
    try:
        await AuthService(db).register_user(data=data)
    except UserAlreadyExistsException:
        raise UserAlreadyExistsHTTPException
    return {"status": "ok"}


@router.post("/login")
async def login(db: DBDep, data: UserLogin, response: Response):
    try:
        access_token = await AuthService(db).login_user(data=data)
    except UserDoesNotExistException:
        raise UserDoesNotExistHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    response.set_cookie("access_token", access_token, httponly=True)

    return {"status": "ok", "access_token": access_token}


@router.get("/profile")
async def get_me(db: DBDep, user_id: UserIdDep):
    return await AuthService(db).get_me(user_id)


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "ok"}
