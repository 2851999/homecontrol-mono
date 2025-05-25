from typing import Optional

from homecontrol_base_api.database.core import DatabaseSession

from homecontrol_auth.database.user_sessions import UserSessionsSession
from homecontrol_auth.database.users import UsersSession


class AuthDatabaseSession(DatabaseSession):
    """Handles an authentication database session"""

    _users: Optional[UsersSession] = None
    _user_sessions: Optional[UserSessionsSession] = None

    @property
    def users(self) -> UsersSession:
        if not self._users:
            self._users = UsersSession(self._session)
        return self._users

    @property
    def user_sessions(self) -> UserSessionsSession:
        if not self._user_sessions:
            self._user_sessions = UserSessionsSession(self._session)
        return self._user_sessions
