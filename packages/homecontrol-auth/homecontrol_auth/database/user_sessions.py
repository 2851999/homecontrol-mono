
from homecontrol_base_api.database.core import DatabaseSession

from homecontrol_auth.database.models import UserSessionInDB


class UserSessionsSession(DatabaseSession):
    """Handles user sessions in the database"""

    async def create(self, user_session: UserSessionInDB) -> UserSessionInDB:
        """Creates a user session in the database
        
        :param user_session: User session to create
        :returns: Created user session
        """

        self._session.add(user_session)
        await self._session.commit()
        await self._session.refresh(user_session)
        return user_session