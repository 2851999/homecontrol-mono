from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator, Optional

from fastapi import Depends
from homecontrol_auth.service.users import UsersService
from homecontrol_auth.database.core import AuthDatabaseSession
from homecontrol_base_api.database.core import Database, get_database
from homecontrol_auth.config import settings


class AuthService:
    """Service that handles authentication"""

    _session: AuthDatabaseSession

    _users: Optional[UsersService] = None

    def __init__(self, session: AuthDatabaseSession):
        self._session = session

    @property
    def users(self) -> UsersService:
        if not self._users:
            self._users = UsersService(self._session)
        return self._users


async def get_auth_service() -> AsyncGenerator[AuthService, None]:
    """Creates an instance of the auth service"""

    async with get_database(AuthDatabaseSession, settings.database) as database:
        async with database.start_session() as session:
            yield AuthService(session)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
