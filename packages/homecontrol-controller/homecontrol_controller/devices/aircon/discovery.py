from msmart.discover import Discover
from pydantic import TypeAdapter

from homecontrol_controller.config import MideaSettings
from homecontrol_controller.database.models import ACDeviceInDB
from homecontrol_controller.exceptions import DeviceConnectionError, DeviceDiscoveryError, DeviceNotFoundError
from homecontrol_controller.schemas.aircon import ACDeviceDiscoveryInfo


class ACDiscovery:
    """Contains methods to discover AC devices."""

    @staticmethod
    async def discover(settings: MideaSettings) -> ACDeviceDiscoveryInfo:
        """Attempts to discover an air conditioning device given its ip address

        :param settings: Midea settings for authentication.
        :returns: Database model of the discovered device.
        :raises DeviceConnectionError: If an error occurs when trying to connect to the device.
        """

        # Have previously found can be temperamental returning None when repeating will find it, so retry up to 3 times here
        found_devices = []
        attempts = 0
        while len(found_devices) == 0 and attempts < 3:
            try:
                found_devices = await Discover.discover(
                    account=settings.username, password=settings.password.get_secret_value()
                )
            except Exception:
                raise DeviceDiscoveryError(f"An error occurred while attempting to discover air conditioning units")
            attempts += 1

        return TypeAdapter(list[ACDeviceDiscoveryInfo]).validate_python(found_devices)

    @staticmethod
    async def discover_single(name: str, ip_address: str, settings: MideaSettings) -> ACDeviceInDB:
        """Attempts to discover an air conditioning device given its ip address

        :param name: Name to give the device.
        :param ip_address: IP address of the device.
        :param settings: Midea settings for authentication.
        :returns: Database model of the discovered device.
        :raises DeviceConnectionError: If an error occurs when trying to connect to the device.
        :raises DeviceNotFoundError: If the device is not found.
        """

        # Have previously found can be temperamental returning None when repeating will find it, so retry up to 3 times here
        found_device = None
        attempts = 0
        while found_device is None and attempts < 3:
            try:
                found_device = await Discover.discover_single(
                    ip_address, account=settings.username, password=settings.password.get_secret_value()
                )
            except Exception:
                raise DeviceConnectionError(
                    f"An error occurred while attempting to discover an air conditioning unit at {ip_address}"
                )
            attempts += 1

        if found_device is None or found_device.key is None or found_device.token is None:
            raise DeviceNotFoundError(f"Unable to discover the air conditioning unit at {ip_address}")

        return ACDeviceInDB(
            name=name,
            ip_address=ip_address,
            port=found_device.port,
            identifier=found_device.id,
            key=found_device.key,
            token=found_device.token,
        )
