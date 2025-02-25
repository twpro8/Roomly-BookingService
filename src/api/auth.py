from fastapi import APIRouter, Response

from src.api.dependencies import UserIdDep
from src.exceptions import (
    UserAlreadyExistsHTTPException,
    UserDoesNotExistHTTPException,
    IncorrectPasswordHTTPException,
    UserAlreadyExistsException,
    UserDoesNotExistException,
    IncorrectPasswordException,
    EmailAlreadyExistsHTTPException,
    EmailAlreadyExistsException,
    UsernameAlreadyExistsHTTPException,
    UsernameAlreadyExistsException,
)
from src.schemas.users import UserRequestAddDTO, UserLoginDTO, UserPatchRequestDTO
from src.services.auth import AuthService

from src.api.dependencies import DBDep


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", summary="📝 Sign up")
async def register(db: DBDep, data: UserRequestAddDTO):
    try:
        await AuthService(db).register_user(data=data)
    except UserAlreadyExistsException:
        raise UserAlreadyExistsHTTPException
    return {"status": "ok"}


@router.post("/login", summary="🔑 Log in")
async def login(db: DBDep, data: UserLoginDTO, response: Response):
    try:
        access_token = await AuthService(db).login_user(data=data)
    except UserDoesNotExistException:
        raise UserDoesNotExistHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    response.set_cookie("access_token", access_token, httponly=True)

    return {"status": "ok", "access_token": access_token}


@router.get("/me", summary="👨‍💻 My profile")
async def get_me(db: DBDep, user_id: UserIdDep):
    return await AuthService(db).get_me(user_id)


@router.patch("/me", summary="⚙️ Edit my profile")
async def partly_edit_user(db: DBDep, user_id: UserIdDep, data: UserPatchRequestDTO):
    try:
        await AuthService(db).partly_edit_user(user_id=user_id, data=data)
    except UsernameAlreadyExistsException:
        raise UsernameAlreadyExistsHTTPException
    except EmailAlreadyExistsException:
        raise EmailAlreadyExistsHTTPException
    return {"status": "ok"}


@router.post("/logout", summary="🔒 Log out")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "ok"}
