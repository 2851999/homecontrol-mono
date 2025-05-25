from uuid import UUID

from homecontrol_base_api.database.core import DatabaseSession
from homecontrol_base_api.exceptions import NoRecordFound
from sqlalchemy import delete, exc, select

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

    async def get(self, session_id: str) -> UserSessionInDB:
        """Returns a user session from the database given its ID

        :param session_id: ID of the user session to get
        :returns: The user session
        :raises NoRecordFound: If the user session with the given ID is not found in the database
        """

        try:
            return (
                await self._session.execute(select(UserSessionInDB).where(UserSessionInDB.id == UUID(session_id)))
            ).scalar_one()
        except exc.NoResultFound:
            raise NoRecordFound(f"No user session found with the ID '{session_id}'")

    async def update(self, user_session: UserSessionInDB) -> UserSessionInDB:
        """Updates a user session by commiting any changes to the database

        :param user_session: User session to update
        :returns: The user session
        """

        await self._session.commit()
        await self._session.refresh(user_session)
        return user_session

    async def delete(self, session_id: str) -> None:
        """Deletes a user session from the database given its ID

        :param session_id: ID of the session to delete
        """

        await self._session.execute(delete(UserSessionInDB).where(UserSessionInDB.id == UUID(session_id)))
        await self._session.commit()
