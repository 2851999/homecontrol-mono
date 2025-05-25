from pydantic import TypeAdapter

from homecontrol_auth import security
from homecontrol_auth.database.core import AuthDatabaseSession
from homecontrol_auth.database.models import UserInDB
from homecontrol_auth.schemas.users import User, UserAccountType, UserPost


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

        # Create the user
        user_out = await self._session.users.create(
            UserInDB(
                username=user.username,
                hashed_password=security.hash_password(user.password.get_secret_value()),
                account_type=UserAccountType.ADMIN if is_first_user else UserAccountType.DEFAULT,
                enabled=is_first_user,
            )
        )

        return User.model_validate(user_out)

    async def get(self, user_id: str) -> User:
        """Returns a user given its ID

        :param user_id: ID of the user to get
        :returns: The user
        """

        return User.model_validate(await self._session.users.get(user_id))

    async def get_all(self) -> list[User]:
        """Returns a list of users

        :returns: List of users
        """

        return TypeAdapter(list[User]).validate_python(await self._session.users.get_all())
