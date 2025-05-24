import asyncio

from pydantic_settings import BaseSettings, SettingsConfigDict

from homecontrol_auth.database.core import AuthDatabaseSession
from homecontrol_auth.database.models import Base
from homecontrol_base_api.config.core import DatabaseSettings, get_database_url
from homecontrol_base_api.database.core import get_database
from homecontrol_auth.service.core import AuthService, get_auth_service
from homecontrol_auth.schemas.users import UserPost
from homecontrol_auth.config import Settings


# async def async_main():
#     async with get_database(AuthDatabaseSession) as database:
#         async with database.connect() as conn:
#             await conn.run_sync(Base.metadata.create_all)

#         # async with get_auth_service(database) as auth_service:
#         #     user = await auth_service.users.create(UserPost(username="Test2", password="Test2"))
#         #     print(user)


# asyncio.run(async_main())
settings = Settings()
print(settings)
print(get_database_url(settings.database))