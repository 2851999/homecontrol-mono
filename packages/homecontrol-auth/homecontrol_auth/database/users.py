from sqlalchemy import func, select
from homecontrol_auth.database.models import UserInDB
from homecontrol_base_api.database.core import DatabaseSession
from sqlalchemy.exc import IntegrityError

from homecontrol_base_api.exceptions import DuplicateRecordError


class UsersSession(DatabaseSession):
    """Handles users in the database"""

    async def create(self, user: UserInDB) -> UserInDB:
        """Creates a user in the database

        :param user: User to create
        :returns: Created user
        :raises DuplicateRecordError: If a user with the same username already exists
        """

        self._session.add(user)
        try:
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            raise DuplicateRecordError(f"User with username '{user.username}' already exists") from exc
        await self._session.refresh(user)
        return user
    
    async def get_by_username(self, username: str) -> UserInDB:
        """Returns a user from the database given their username
        
        :param username: Username of the user to get
        :returns: The User
        """

        return (await self._session.execute(select(UserInDB).where(UserInDB.username == username))).scalar_one() 

    async def count(self) -> int:
        """Counts the number of users

        :returns: Number of users
        """

        return (await self._session.execute(select(func.count()).select_from(UserInDB))).scalar_one()
