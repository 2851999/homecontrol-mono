from datetime import datetime, timedelta, timezone
from uuid import uuid4

from fastapi import Response
from homecontrol_auth.database.core import AuthDatabaseSession

from homecontrol_auth.schemas.user_sessions import InternalUserSession, LoginPost, UserSession
from homecontrol_auth.security import generate_jwt, verify_password
from homecontrol_auth.exceptions import AuthenticationError
from homecontrol_auth.database.models import UserInDB, UserSessionInDB
from homecontrol_auth.config import settings
from homecontrol_auth.schemas.users import UserAccountType
from homecontrol_base_api.exceptions import NoRecordFound


class UserSessionsService:
    """Service that handles user sessions"""

    _session: AuthDatabaseSession

    def __init__(self, session: AuthDatabaseSession):
        self._session = session

    def _generate_token(self, session_id: str, expiry_time: datetime) -> str:
        """Generates and returns an access token
        
        :param session_id: ID of the session the access token should be generated for
        :returns: The generated access token
        """

        return generate_jwt(payload={"session_id": session_id, "exp": expiry_time}, key=settings.secret_key.get_secret_value())

    async def _create_internal_user_session(self, user: UserInDB, long_lived: bool) -> InternalUserSession:
        """Creates an internal user session
        
        :param user: User to create the session for
        :param long_lived: Whether the session should be long lived or not
        :returns: The created internal user session
        """

        session_id = uuid4()
        current_time = datetime.now(timezone.utc)
        expiry_time = current_time + timedelta(seconds=settings.long_lived_refresh_token_expiry_seconds if long_lived else settings.refresh_token_expiry_seconds)

        user_session = UserSessionInDB(
            id=session_id,
            user_id=user.id,
            access_token=self._generate_token(str(session_id), current_time + timedelta(seconds=settings.access_token_expiry_seconds)),
            refresh_token=self._generate_token(str(session_id), expiry_time),
            long_lived=long_lived,
            expiry_time=expiry_time
        )

        user_session = await self._session.user_sessions.create(user_session)
        return InternalUserSession.model_validate(user_session)

    def _assign_internal_session_tokens(self, internal_user_session: InternalUserSession, response: Response):
        """Assigns the tokens in an internal user session to the HTTP response as cookies
        
        :param internal_user_session: Internal user session containing the tokens
        :param response: FastAPI response object to set the cookies on
        """

        # Stored time doesn't have timezone, so add UTC here as required for cookie
        session_expire_time_utc = internal_user_session.expiry_time.replace(
            tzinfo=timezone.utc
        )
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

    async def create_session(self, login: LoginPost, response: Response) -> UserSession:
        """Creates a user session

        :param login: Login information
        :param response: FastAPI response object to set the cookies on
        :returns: Created user session
        """

        user = None
        try:
            user = await self._session.users.get_by_username(login.username)
        except NoRecordFound:
            # Ignore if not found as want to give an AuthenticationError below instead
            pass

        # Verify the password
        if user is None or not verify_password(login.password.get_secret_value(), user.hashed_password):
            raise AuthenticationError("Invalid username or password")
        
        # Verify the account is enabled
        if not user.enabled:
            raise AuthenticationError("Account is disabled. Please contact an admin.")
        
        # Create the session
        internal_user_session = await self._create_internal_user_session(user, long_lived=login.long_lived if user.account_type == UserAccountType.DEFAULT else False)

        # Assign the session tokens
        self._assign_internal_session_tokens(internal_user_session, response)

        return UserSession.model_validate(internal_user_session)