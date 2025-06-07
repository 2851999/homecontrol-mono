from fastapi import status
from homecontrol_base_api.exceptions import BaseAPIError


class DeviceDiscoveryError(BaseAPIError):
    """Raised when an error occurs while attempting to discover devices"""

    status_code = status.HTTP_502_BAD_GATEWAY


class DeviceConnectionError(BaseAPIError):
    """Raised when an error occurs while attempting to connect to a device"""

    status_code = status.HTTP_404_NOT_FOUND


class DeviceNotFoundError(BaseAPIError):
    """Raised when a device isnt found while attempting to connect to it or when it isnt found in the existing devices."""

    status_code = status.HTTP_404_NOT_FOUND


class DeviceAuthenticationError(BaseAPIError):
    """Raised when an error occurs while attempting to authenticate a device"""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class DeviceInvalidStateError(BaseAPIError):
    """Raised when attempting to change the state of a device to be invalid"""

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
