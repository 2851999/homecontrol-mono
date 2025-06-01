from fastapi import status
from homecontrol_base_api.exceptions import BaseAPIError


class DeviceConnectionError(BaseAPIError):
    """Raised when an error occurs while attempting to connect to a device"""

    status_code = status.HTTP_404_NOT_FOUND


class DeviceNotFoundError(BaseAPIError):
    """Raised when a device isnt found while attempting to connect to it or when it isnt found in the existing devices."""

    status_code = status.HTTP_404_NOT_FOUND


class DeviceAuthenticationError(BaseAPIError):
    """Raised when an error occurs while attempting to authenticate a device"""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
