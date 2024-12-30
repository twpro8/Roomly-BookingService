from fastapi import HTTPException
from sqlalchemy import insert, select, update, delete
from pydantic import BaseModel


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        res = await self.session.execute(query)

        return [self.schema.model_validate(model, from_attributes=True) for model in res.scalars().all()]

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(query)
        model = res.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True)

    async def add(self, data: BaseModel):
        stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
        )
        res = await self.session.execute(stmt)
        model = res.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        stmt = (
            update(self.model)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .filter_by(**filter_by))
        res = await self.session.execute(stmt)
        if res.rowcount != 1:
            raise HTTPException(status_code=404, detail="Hotel not found")

    async def delete(self, **filter_by) -> None:
        stmt = delete(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        if res.rowcount != 1:
            raise HTTPException(status_code=404, detail="Hotel not found")
