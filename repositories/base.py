from fastapi import HTTPException
from sqlalchemy import insert, select, update, delete
from pydantic import BaseModel

class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        res = await self.session.execute(query)

        return res.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(query)

        return res.scalars().one_or_none()

    async def add(self, data: BaseModel):
        stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
        )
        res = await self.session.execute(stmt)
        return res.scalars().one()

    async def edit(self, data: BaseModel, **filter_by) -> None:
        stmt = update(self.model).values(**data.model_dump()).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        if res.rowcount != 1:
            raise HTTPException(status_code=404, detail="Hotel not found")


    async def delete(self, id: int) -> None:
        stmt = delete(self.model).filter_by(id=id)
        res = await self.session.execute(stmt)
        if res.rowcount != 1:
            raise HTTPException(status_code=404, detail="Hotel not found")
