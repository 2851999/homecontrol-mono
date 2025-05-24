from sqlalchemy import func, select
from homecontrol_auth.database.models import UserInDB
from homecontrol_base_api.database.core import DatabaseSession
from sqlalchemy.exc import IntegrityError

from homecontrol_base_api.database.exceptions import DuplicateRecordError

class UsersSession(DatabaseSession):
    """Handles users in the database"""

    async def create(self, user: UserInDB) -> UserInDB:
        """Creates a user in the database
        
        :param user: User to create
        :returns: Created user
        """

        self._session.add(user)
        try:
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            raise DuplicateRecordError(f"User with username {user.username} already exists") from exc
        await self._session.refresh(user)
        return user
    
    async def count(self) -> int:
        """Counts the number of users
        
        :returns: Number of users
        """

        return (await self._session.execute(select(func.count()).select_from(UserInDB))).scalar_one()