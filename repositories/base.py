from sqlalchemy import insert, select


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

    async def add(self, data):
        stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
        )
        res = await self.session.execute(stmt)

        return res.scalars().one()
