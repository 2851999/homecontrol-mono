from contextlib import asynccontextmanager, contextmanager
from typing import AsyncGenerator, Generic, Type, TypeVar
import uuid
from functools import lru_cache
import asyncio

from pydantic.dataclasses import dataclass
from sqlalchemy import Column, Uuid
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine

from homecontrol_base_api.config.core import load_config

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


class DatabaseConnection:
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session


class TestDatabaseConnection(DatabaseConnection):
    async def create(self):
        data = TestModel(id=uuid.uuid4())
        self._session.add(data)
        await self._session.commit()
        await self._session.refresh(data)
        return data


TDatabaseConnection = TypeVar("TDatabaseConnection", bound=DatabaseConnection)

# See https://medium.com/@tclaitken/setting-up-a-fastapi-app-with-async-sqlalchemy-2-0-pydantic-v2-e6c540be4308 on how to use for FastAPI
# and https://praciano.com.br/fastapi-and-async-sqlalchemy-20-with-pytest-done-right.html


class Database(Generic[TDatabaseConnection]):

    _engine: AsyncEngine
    _session_maker: sessionmaker
    _connection_type = Type[TDatabaseConnection]

    def __init__(self, connection_type: Type[TDatabaseConnection]):
        self._engine = create_async_engine("sqlite+aiosqlite:///database.db")
        self._session_maker = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )
        self._connection_type = connection_type

    async def _init(self):
        """This method is required in order to be able to call async methods"""
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def _del(self):
        await self._engine.dispose()
        self._engine = None
        self._session_maker = None

    @asynccontextmanager
    async def connect(self) -> AsyncGenerator[TDatabaseConnection, None]:
        async with self._session_maker() as session:
            try:
                await session.begin()
                yield self._connection_type(session)
            finally:
                await session.close()


# # Effectively would need the following for a service
# database: Database = Database()

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     yield
#     if database._engine is not None:
#         # Close the DB connection
#         await database.close()


# Or this for an individual invocation
@asynccontextmanager
async def get_database(
    connection_type: Type[TDatabaseConnection],
) -> AsyncGenerator[Database[TDatabaseConnection], None]:
    database = Database[TDatabaseConnection](connection_type)
    await database._init()
    try:
        yield database
    finally:
        await database._del()


async def async_main():
    async with get_database(TestDatabaseConnection) as database:
        async with database.connect() as conn:
            await conn.create()


asyncio.run(async_main())
