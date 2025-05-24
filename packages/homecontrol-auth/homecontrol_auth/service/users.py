from homecontrol_auth.database.core import AuthDatabaseSession
from homecontrol_auth.schemas.users import User, UserAccountType, UserPost
from homecontrol_auth.database.models import UserInDB


class UsersService:
    """Service that handles users"""

    _session: AuthDatabaseSession

    def __init__(self, session: AuthDatabaseSession):
        self._session = session

    async def create(self, user: UserPost) -> User:
        """Creates a user
        
        :param user: User to create
        :returns: Created user
        """

        # Check if its the first user
        is_first_user = await self._session.users.count() == 0

        # TODO: Handle errors
        user_out = await self._session.users.create(UserInDB(username=user.username, hashed_password="SOMETHING", account_type=UserAccountType.ADMIN if is_first_user else UserAccountType.DEFAULT, enabled=is_first_user))

        return User.model_validate(user_out)