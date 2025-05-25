from typing import Annotated
from fastapi import Cookie, Depends

from homecontrol_auth.exceptions import AuthenticationError, InsufficientPrivilegesError
from homecontrol_auth.schemas.users import User, UserAccountType
from homecontrol_auth.schemas.user_sessions import UserSession
from homecontrol_auth.service.core import AuthServiceDep


def get_access_token_from_cookie(access_token: Annotated[str, Cookie()] = None) -> str:
    """Verifies there is an access token in the cookie parameters and returns it"""

    if access_token is None:
        raise AuthenticationError("No access token provided")
    auth = access_token.split(" ")
    if auth[0].lower() != "bearer" or len(auth) != 2:
        raise AuthenticationError("Invalid bearer token provided")
    return auth[1]


def get_refresh_token_from_cookie(refresh_token: Annotated[str, Cookie()] = None) -> str:
    """Verifies there is a refresh token in the cookie parameters and returns it"""

    if refresh_token is None:
        raise AuthenticationError("No refresh token provided")
    return refresh_token


AccessToken = Annotated[str, Depends(get_access_token_from_cookie)]
RefreshToken = Annotated[str, Depends(get_refresh_token_from_cookie)]


async def verify_current_user_session(auth_service: AuthServiceDep, access_token: AccessToken) -> UserSession:
    """Verifies the current user"""

    return await auth_service.verify_session(access_token)


async def verify_current_user(auth_service: AuthServiceDep, access_token: AccessToken) -> User:
    """Verifies the current user"""

    return await auth_service.verify(access_token)


def _create_verify_user_type_dep(valid_account_type: UserAccountType):
    """Returns a dependency that validates the current user and ensures they also have a specific account type"""

    async def user_type_dep(user: Annotated[User, Depends(verify_current_user)]) -> User:
        if user.account_type != valid_account_type:
            raise InsufficientPrivilegesError("Insufficient privileges")
        return user

    return user_type_dep


verify_admin_user = _create_verify_user_type_dep(UserAccountType.ADMIN)

AnySession = Annotated[UserSession, Depends(verify_current_user_session)]
AnyUser = Annotated[User, Depends(verify_current_user)]
AdminUser = Annotated[User, Depends(verify_admin_user)]
