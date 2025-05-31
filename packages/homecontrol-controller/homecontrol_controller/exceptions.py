from fastapi import status
from homecontrol_base_api.exceptions import BaseAPIError


class DeviceConnectionError(BaseAPIError):
    """Raised when an error occurs while attempting to connect to a device"""

    status_code = status.HTTP_404_NOT_FOUND


class DeviceNotFoundError(BaseAPIError):
    """Raised when a device isnt found while attempting to connect to it"""

    status_code = status.HTTP_404_NOT_FOUND
