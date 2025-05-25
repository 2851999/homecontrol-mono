from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator, Optional

from fastapi import Depends
from homecontrol_auth.service.users import UsersService
from homecontrol_auth.database.core import AuthDatabaseSession
from homecontrol_base_api.database.core import get_database
from homecontrol_auth.config import settings
from homecontrol_auth.service.user_sessions import UserSessionsService
from homecontrol_auth.schemas.users import User
from homecontrol_auth.exceptions import AuthenticationError


class AuthService:
    """Service that handles authentication"""

    _session: AuthDatabaseSession

    _users: Optional[UsersService] = None
    _user_sessions: Optional[UserSessionsService] = None

    def __init__(self, session: AuthDatabaseSession):
        self._session = session

    @property
    def users(self) -> UsersService:
        if not self._users:
            self._users = UsersService(self._session)
        return self._users

    @property
    def user_sessions(self) -> UserSessionsService:
        if not self._user_sessions:
            self._user_sessions = UserSessionsService(self._session)
        return self._user_sessions

    async def verify(self, access_token: str) -> User:
        """Verifies given an access token
        
        :param access_token: Access token to authenticate
        :returns: The user
        """
        user_session = await self.user_sessions.verify_session(access_token)
        user = await self.users.get(user_session.user_id)

        if not user.enabled:
            raise AuthenticationError("User is disabled")
        
        return user


# TODO: Move into dependencies?
async def get_auth_service() -> AsyncGenerator[AuthService, None]:
    """Creates an instance of the auth service"""

    async with get_database(AuthDatabaseSession, settings.database) as database:
        async with database.start_session() as session:
            yield AuthService(session)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
