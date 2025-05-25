import asyncio
import uuid
from contextlib import asynccontextmanager, contextmanager
from functools import lru_cache
from typing import AsyncGenerator, Generic, Type, TypeVar

from pydantic.dataclasses import dataclass
from sqlalchemy import Column, Uuid
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from homecontrol_base_api.config.core import load_config
from homecontrol_base_api.database.core import DatabaseSession, get_database

# @dataclass
# class TestConfigData:
#     value: str


# @lru_cache
# def get_test_settings() -> TestConfigData:
#     return load_config("test.json", TestConfigData)


# print(get_test_settings())


Base = declarative_base()


class TestModel(Base):
    __tablename__ = "test"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)


class TestDatabaseSession(DatabaseSession):
    async def create(self):
        data = TestModel(id=uuid.uuid4())
        self._session.add(data)
        await self._session.commit()
        await self._session.refresh(data)
        return data


async def async_main():
    async with get_database(TestDatabaseSession) as database:
        async with database.connect() as conn:
            await conn.run_sync(Base.metadata.create_all)

        async with database.start_session() as session:
            await session.create()


asyncio.run(async_main())
