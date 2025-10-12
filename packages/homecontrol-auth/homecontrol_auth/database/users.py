from uuid import UUID

from homecontrol_base_api.database.core import DatabaseSession
from homecontrol_base_api.exceptions import DuplicateRecordError, RecordNotFoundError
from sqlalchemy import delete
from sqlalchemy import exc as sqlalchemy_exc
from sqlalchemy import func, select

from homecontrol_auth.database.models import UserInDB


class UsersSession(DatabaseSession):
    """Handles users in the database"""

    async def create(self, user: UserInDB) -> UserInDB:
        """Creates a user in the database

        :param user: User to create
        :return: Created user
        :raises DuplicateRecordError: If a user with the same username already exists
        """

        self._session.add(user)
        try:
            await self._session.commit()
        except sqlalchemy_exc.IntegrityError as exc:
            await self._session.rollback()
            raise DuplicateRecordError(f"User with username '{user.username}' already exists") from exc
        await self._session.refresh(user)
        return user

    async def get(self, user_id: str) -> UserInDB:
        """Returns a user from the database given its ID

        :param user_id: ID of the user to get
        :return: The user
        :raises RecordNotFoundError: If the user with the given ID is not found in the database
        """

        try:
            return (await self._session.execute(select(UserInDB).where(UserInDB.id == UUID(user_id)))).scalar_one()
        except (sqlalchemy_exc.NoResultFound, ValueError) as exc:
            raise RecordNotFoundError(f"No user found with the ID '{user_id}'") from exc

    async def get_by_username(self, username: str) -> UserInDB:
        """Returns a user from the database given their username

        :param username: Username of the user to get
        :return: The User
        :raises RecordNotFoundError: If a user with the given username is not found in the database
        """

        try:
            return (await self._session.execute(select(UserInDB).where(UserInDB.username == username))).scalar_one()
        except sqlalchemy_exc.NoResultFound:
            raise RecordNotFoundError(f"No user found with the username '{username}'")

    async def count(self) -> int:
        """Counts the number of users

        :return: Number of users
        """

        return (await self._session.execute(select(func.count()).select_from(UserInDB))).scalar_one()

    async def get_all(self) -> list[UserInDB]:
        """Returns a list of users

        :return: List of users
        """

        return (await self._session.execute(select(UserInDB))).scalars().all()

    async def update(self, user: UserInDB) -> UserInDB:
        """Updates a user by commiting any changes to the database

        :param user: User to update
        :return: The user
        """

        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def delete(self, user_id: str) -> None:
        """Deletes a user from the database given its ID

        :param user_id: ID of the user to delete
        """

        try:
            result = await self._session.execute(delete(UserInDB).where(UserInDB.id == UUID(user_id)))
        except ValueError as exc:
            raise RecordNotFoundError(f"No user found with the ID '{user_id}'") from exc

        if result.rowcount == 0:
            raise RecordNotFoundError(f"No user found with the ID '{user_id}'")

        await self._session.commit()
