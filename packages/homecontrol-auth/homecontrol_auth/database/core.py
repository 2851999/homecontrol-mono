
from typing import Optional
from homecontrol_auth.database.users import UsersSession
from homecontrol_base_api.database.core import Database, DatabaseSession, get_database

class AuthDatabaseSession(DatabaseSession):
    """Handles an authentication database session"""

    _users: Optional[UsersSession] = None

    @property
    def users(self) -> UsersSession:
        if not self._users:
            self._users = UsersSession(self._session)
        return self._users

auth_database: Database[AuthDatabaseSession] = get_database(AuthDatabaseSession)