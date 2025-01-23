from sqlalchemy import insert, select, update, delete
from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound, IntegrityError

from src.exceptions import ObjectNotFoundException, ObjectAlreadyExistsException
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    schema: BaseModel = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in res.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(query)
        model = res.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(query)
        try:
            model = res.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel):
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            res = await self.session.execute(stmt)
        except IntegrityError:
            raise ObjectAlreadyExistsException
        model = res.scalars().one()
        return self.mapper.map_to_domain_entity(model)

    async def add_bulk(self, data: list[BaseModel]):
        stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(stmt)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        stmt = (
            update(self.model)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .filter_by(**filter_by)
        )
        await self.session.execute(stmt)

    async def delete(self, **filter_by) -> None:
        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)
