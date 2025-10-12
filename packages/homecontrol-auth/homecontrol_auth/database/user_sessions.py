from datetime import datetime
from uuid import UUID

from homecontrol_base_api.database.core import DatabaseSession
from homecontrol_base_api.exceptions import RecordNotFoundError
from sqlalchemy import delete
from sqlalchemy import exc as sqlalchemy_exc
from sqlalchemy import select

from homecontrol_auth.database.models import UserSessionInDB


class UserSessionsSession(DatabaseSession):
    """Handles user sessions in the database"""

    async def create(self, user_session: UserSessionInDB) -> UserSessionInDB:
        """Creates a user session in the database

        :param user_session: User session to create
        :return: Created user session
        """

        self._session.add(user_session)
        await self._session.commit()
        await self._session.refresh(user_session)
        return user_session

    async def get(self, session_id: str) -> UserSessionInDB:
        """Returns a user session from the database given its ID

        :param session_id: ID of the user session to get
        :return: The user session
        :raises RecordNotFoundError: If the user session with the given ID is not found in the database
        """

        try:
            return (
                await self._session.execute(select(UserSessionInDB).where(UserSessionInDB.id == UUID(session_id)))
            ).scalar_one()
        except (sqlalchemy_exc.NoResultFound, ValueError) as exc:
            raise RecordNotFoundError(f"No user session found with the ID '{session_id}'") from exc

    async def update(self, user_session: UserSessionInDB) -> UserSessionInDB:
        """Updates a user session by commiting any changes to the database

        :param user_session: User session to update
        :return: The user session
        """

        await self._session.commit()
        await self._session.refresh(user_session)
        return user_session

    async def delete(self, session_id: str) -> None:
        """Deletes a user session from the database given its ID

        :param session_id: ID of the session to delete
        :raises RecordNotFoundError: If the user session with the given ID is not found in the database
        """

        try:
            result = await self._session.execute(delete(UserSessionInDB).where(UserSessionInDB.id == UUID(session_id)))
        except ValueError as exc:
            raise RecordNotFoundError(f"No user session found with the ID '{session_id}'") from exc

        if result.rowcount == 0:
            raise RecordNotFoundError(f"No user session found with the ID '{session_id}'")

        await self._session.commit()

    async def delete_all_expired_before(self, datetime_value: datetime) -> int:
        """Deletes all user sessions from the database that have expired before the given time

        :param datetime_value: Date and time before which sessions that have expired should be deleted
        :return: Number of rows deleted
        """
        return (
            await self._session.execute(delete(UserSessionInDB).where(UserSessionInDB.expiry_time < datetime_value))
        ).rowcount
