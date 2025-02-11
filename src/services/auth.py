from datetime import datetime, timezone, timedelta

from fastapi import HTTPException
import jwt

from src.config import settings
from passlib.context import CryptContext

from src.exceptions import (
    ObjectAlreadyExistsException,
    UserAlreadyExistsException,
    UserDoesNotExistException,
    IncorrectPasswordException,
)
from src.schemas.users import UserRequestAdd, AddUser, UserLogin
from src.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(
            to_encode, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Signature has expired")

    async def register_user(self, data: UserRequestAdd) -> None:
        normalized_email = data.email.strip().lower()
        hashed_password = self.hash_password(data.password)

        new_user_data = AddUser(
            username=data.username, email=normalized_email, hashed_password=hashed_password
        )
        try:
            await self.db.users.add(new_user_data)
        except ObjectAlreadyExistsException:
            raise UserAlreadyExistsException
        await self.db.commit()

    async def login_user(self, data: UserLogin):
        user = await self.db.users.get_user_with_hashed_password(username=data.username)
        if not user:
            raise UserDoesNotExistException
        if not self.verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordException
        return self.create_access_token({"user_id": user.id})

    async def get_me(self, user_id: int):
        return await self.db.users.get_one_or_none(id=user_id)
