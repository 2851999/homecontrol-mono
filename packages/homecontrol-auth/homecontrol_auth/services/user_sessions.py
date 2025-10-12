from datetime import datetime, timedelta, timezone
from uuid import uuid4

from fastapi import Response
from homecontrol_base_api.exceptions import RecordNotFoundError

from homecontrol_auth.config import settings
from homecontrol_auth.database.core import AuthDatabaseSession
from homecontrol_auth.database.models import UserInDB, UserSessionInDB
from homecontrol_auth.exceptions import AuthenticationError
from homecontrol_auth.schemas.user_sessions import InternalUserSession, LoginPost, UserSession
from homecontrol_auth.schemas.users import UserAccountType
from homecontrol_auth.security import generate_jwt, verify_jwt, verify_password


class UserSessionsService:
    """Service that handles user sessions"""

    _session: AuthDatabaseSession

    def __init__(self, session: AuthDatabaseSession):
        self._session = session

    def _generate_token(self, session_id: str, expiry_time: datetime) -> str:
        """Generates and returns an access token

        :param session_id: ID of the session the access token should be generated for
        :return: The generated access token
        """

        return generate_jwt(
            payload={"session_id": session_id, "exp": expiry_time}, key=settings.secret_key.get_secret_value()
        )

    async def _create_internal(self, user: UserInDB, long_lived: bool) -> InternalUserSession:
        """Creates an internal user session

        :param user: User to create the session for
        :param long_lived: Whether the session should be long lived or not
        :return: The created internal user session
        """

        session_id = uuid4()
        current_time = datetime.now(timezone.utc)
        expiry_time = current_time + timedelta(
            seconds=(
                settings.long_lived_refresh_token_expiry_seconds
                if long_lived
                else settings.refresh_token_expiry_seconds
            )
        )

        user_session = UserSessionInDB(
            id=session_id,
            user_id=user.id,
            access_token=self._generate_token(
                str(session_id), current_time + timedelta(seconds=settings.access_token_expiry_seconds)
            ),
            refresh_token=self._generate_token(str(session_id), expiry_time),
            long_lived=long_lived,
            expiry_time=expiry_time,
        )

        user_session = await self._session.user_sessions.create(user_session)
        return InternalUserSession.model_validate(user_session)

    async def _refresh_internal(self, user_session: UserSessionInDB) -> InternalUserSession:
        """Refreshes an internal user session

        :param user: User to create the session for
        :param long_lived: Whether the session should be long lived or not
        :return: The created internal user session
        """

        current_time = datetime.now(timezone.utc)
        expiry_time = current_time + timedelta(
            seconds=(
                settings.long_lived_refresh_token_expiry_seconds
                if user_session.long_lived
                else settings.refresh_token_expiry_seconds
            )
        )

        user_session.access_token = self._generate_token(
            str(user_session.id), current_time + timedelta(seconds=settings.access_token_expiry_seconds)
        )
        user_session.refresh_token = self._generate_token(str(user_session.id), expiry_time)
        user_session.expiry_time = expiry_time

        user_session = await self._session.user_sessions.update(user_session)
        return InternalUserSession.model_validate(user_session)

    def _assign_session_tokens(self, internal_user_session: InternalUserSession, response: Response):
        """Assigns the tokens in an internal user session to the HTTP response as cookies

        :param internal_user_session: Internal user session containing the tokens
        :param response: FastAPI response object to set the cookies on
        """

        # Stored time doesn't have timezone, so add UTC here as required for cookie
        session_expire_time_utc = internal_user_session.expiry_time.replace(tzinfo=timezone.utc)
        # TODO: Add domain, max age etc
        response.set_cookie(
            key="access_token",
            value=f"Bearer {internal_user_session.access_token.get_secret_value()}",
            expires=session_expire_time_utc,
            httponly=True,
        )
        response.set_cookie(
            key="refresh_token",
            value=internal_user_session.refresh_token.get_secret_value(),
            expires=session_expire_time_utc,
            httponly=True,
        )

    def _remove_session_tokens(self, response: Response):
        """Removes the tokens

        :param response: FastAPI response object to remove the cookies from
        """

        response.delete_cookie(key="access_token")
        response.delete_cookie(key="refresh_token")

    async def create(self, login: LoginPost, response: Response) -> UserSession:
        """Creates a user session

        :param login: Login information
        :param response: FastAPI response object to set the cookies on
        :return: Created user session
        :raises AuthenticationError: If a user with the given username is not found, the password is incorrect or if the user itself is disabled
        """

        user = None
        try:
            user = await self._session.users.get_by_username(login.username)
        except RecordNotFoundError:
            # Ignore if not found as want to give an AuthenticationError below instead
            pass

        # Verify the password
        if user is None or not verify_password(login.password.get_secret_value(), user.hashed_password):
            raise AuthenticationError("Invalid username or password")

        # Verify the account is enabled
        if not user.enabled:
            raise AuthenticationError("Account is disabled. Please contact an admin.")

        # Create the session
        internal_user_session = await self._create_internal(
            user, long_lived=login.long_lived if user.account_type == UserAccountType.DEFAULT else False
        )

        # Assign the session tokens
        self._assign_session_tokens(internal_user_session, response)

        return UserSession.model_validate(internal_user_session)

    async def verify(self, access_token: str) -> UserSession:
        """Verify a user session given its access token

        :param access_token: Access token from the session to verify
        :return: The user sesssion
        :raises AuthenticationError: If the token is invalid
        """

        # Verify the token
        payload = verify_jwt(access_token, settings.secret_key.get_secret_value())

        # Obtain the session to which it belongs
        user_session = await self._session.user_sessions.get(payload["session_id"])

        # Verify the token is the current one for the session
        if user_session.access_token != access_token:
            raise AuthenticationError("Invalid token")

        return UserSession.model_validate(user_session)

    async def refresh(self, refresh_token: str, response: Response) -> UserSession:
        """Refresh a user session given its refresh token

        :param refresh_token: Refresh token from the session to refresh
        :param response: FastAPI response object to set the cookies on
        :return: The user session
        :raises AuthenticationError: If the refresh token has already been used to refresh the session before and is now invalid
        """

        # Verify the token
        payload = verify_jwt(refresh_token, settings.secret_key.get_secret_value())

        # Obtain the user session to which it belongs
        user_session = await self._session.user_sessions.get(payload["session_id"])

        # Verify the current refresh token is the current active one for the session
        if user_session.refresh_token != refresh_token:
            raise AuthenticationError("Invalid token")

        # Refresh the session tokens
        internal_user_session = await self._refresh_internal(user_session)

        # Assign the session tokens
        self._assign_session_tokens(internal_user_session, response)

        return UserSession.model_validate(internal_user_session)

    async def delete(self, session_id: str, response: Response) -> None:
        """Delete a user session given its ID

        :param session_id: ID of the session to delete
        :param response: FastAPI response object to remove the cookies from
        """

        await self._session.user_sessions.delete(session_id)
        self._remove_session_tokens(response)

    async def delete_all_expired(self) -> None:
        """Deletes all user sessions from the database that have expired before now"""

        await self._session.user_sessions.delete_all_expired_before(datetime.now(timezone.utc))
