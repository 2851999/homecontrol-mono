from homecontrol_auth.database.models import UserInDB
from homecontrol_base_api.database.core import DatabaseSession

class UsersSession(DatabaseSession):
    """Handles users in the database"""

    def create(self, user: UserInDB) -> UserInDB:
        """Creates a user in the database"""

        # TODO: Deal with errors
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user