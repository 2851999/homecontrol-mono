import asyncio

from homecontrol_auth.database.core import AuthDatabaseSession
from homecontrol_auth.database.models import Base
from homecontrol_base_api.database.core import get_database


async def async_main():
    async with get_database(AuthDatabaseSession) as database:
        async with database.connect() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # async with database.start_session() as session:
        #     await session.users.create()


asyncio.run(async_main())