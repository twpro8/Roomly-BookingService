from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.users import UsersORM
from src.repositories.mappers.mappers import UserDataMapper, UserWithHashedPasswordDataMapper


class UsersRepository(BaseRepository):
    model = UsersORM
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, username: str):
        query = select(self.model).filter_by(username=username)
        res = await self.session.execute(query)
        model = res.scalars().one()
        return UserWithHashedPasswordDataMapper.map_to_domain_entity(model)
