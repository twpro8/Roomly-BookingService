from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.config import settings


engine = create_async_engine(url=settings.DB_URL)
null_pool_engine = create_async_engine(url=settings.DB_URL, poolclass=NullPool)

session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
null_pool_session_maker = async_sessionmaker(
    bind=null_pool_engine, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass
