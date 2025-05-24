from contextlib import asynccontextmanager
from typing import AsyncGenerator, Generic, Type, TypeVar

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, AsyncConnection
from sqlalchemy.ext.asyncio import create_async_engine

from homecontrol_base_api.config.core import DatabaseSettings, get_database_url


class DatabaseSession:
    """Base class for handling a database session"""

    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        """Initialise

        :param session: Session to use
        """
        self._session = session


TDatabaseSession = TypeVar("TDatabaseConnection", bound=DatabaseSession)


class Database(Generic[TDatabaseSession]):
    """Base class for handling connections to a database"""

    _engine: AsyncEngine
    _session_maker: sessionmaker
    _session_type = Type[TDatabaseSession]

    def __init__(self, session_type: Type[TDatabaseSession], database_settings: DatabaseSettings):
        """Initialise the database engine"""

        self._engine = create_async_engine(get_database_url(database_settings))
        self._session_maker = sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)
        self._session_type = session_type

    async def close(self):
        """This should be called to close any connections to this database"""

        await self._engine.dispose()
        self._engine = None
        self._session_maker = None

    @asynccontextmanager
    async def connect(self) -> AsyncGenerator[AsyncConnection, None]:
        """Starts a new connection with the database"""

        async with self._engine.begin() as conn:
            yield conn

    @asynccontextmanager
    async def start_session(self) -> AsyncGenerator[TDatabaseSession, None]:
        """Starts a new connection with the database"""

        async with self._session_maker() as session:
            try:
                await session.begin()
                yield self._session_type(session)
            finally:
                await session.close()


@asynccontextmanager
async def get_database(
    session_type: Type[TDatabaseSession], settings: DatabaseSettings
) -> AsyncGenerator[Database[TDatabaseSession], None]:
    """Returns a database instance"""

    database = Database(session_type, settings)
    try:
        yield database
    finally:
        await database.close()


# See https://medium.com/@tclaitken/setting-up-a-fastapi-app-with-async-sqlalchemy-2-0-pydantic-v2-e6c540be4308 on how to use for FastAPI
# and https://praciano.com.br/fastapi-and-async-sqlalchemy-20-with-pytest-done-right.html


# # Effectively would need the following for a service
# database: Database = Database()

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     yield
#     if database._engine is not None:
#         # Close the DB connection
#         await database.close()
