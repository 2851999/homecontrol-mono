from fastapi import status

from homecontrol_base_api.exceptions import DatabaseError

class AuthenticationError(DatabaseError):
    """Raised attempting to login with an incorrect username or password"""

    status_code = status.HTTP_401_UNAUTHORIZED