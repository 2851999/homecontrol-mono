from fastapi import status
from homecontrol_base_api.exceptions import BaseAPIError


class AuthenticationError(BaseAPIError):
    """Raised when attempting to login with an incorrect username or password"""

    status_code = status.HTTP_401_UNAUTHORIZED


class InsufficientPrivilegesError(BaseAPIError):
    """Raised when attempting to access something with insufficient privileges"""

    status_code = status.HTTP_403_FORBIDDEN
