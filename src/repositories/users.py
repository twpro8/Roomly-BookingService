from sqlalchemy import select
from pydantic import EmailStr

from src.repositories.base import BaseRepository
from src.models.users import UsersORM
from src.schemas.users import User, UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersORM
    schema = User

    async def get_user_with_hashed_password(self, username: str):
        query = select(self.model).filter_by(username=username)
        res = await self.session.execute(query)
        model = res.scalars().one()
        return UserWithHashedPassword.model_validate(model, from_attributes=True)
