from msmart.discover import Discover

from homecontrol_controller.config import MideaSettings
from homecontrol_controller.database.models import ACDeviceInDB
from homecontrol_controller.devices.aircon.device import ACDevice
from homecontrol_controller.exceptions import DeviceConnectionError, DeviceNotFoundError


class ACManager:
    """Manages a set of air conditioning devices."""

    _devices: dict[str, ACDevice]

    def __init__(self):
        self._devices = {}

    async def add(self, ac_device: ACDeviceInDB) -> ACDevice:
        """Adds an AC device to this manager after first initialising it.

        :param ac_device: Database model of the device to add.
        :returns: The initialised AC device.
        """

        device = ACDevice(ac_device)
        await device.initialise()
        self._devices[str(ac_device.id)] = device
        return device

    async def add_all(self, ac_devices: list[ACDeviceInDB]) -> None:
        """Loads a list of AC devices, adding each to this manager after first intiialising them.

        :param ac_devices: List of database models of the devices to add.
        """
        for ac_device in ac_devices:
            await self.add(ac_device)

    def get(self, device_id: str) -> ACDevice:
        """Returns an AC device given its ID.

        :param device_id: ID of the AC device to get.
        :raises DeviceNotFoundError: If the AC device with the given ID is not found.
        """

        device = self._devices.get(device_id)
        if device is None:
            raise DeviceNotFoundError(f"AC device with ID '{device_id}' was not found")
        return device

    # TODO: Move to discovery.py like Hue?
    @staticmethod
    async def discover(name: str, ip_address: str, settings: MideaSettings) -> ACDeviceInDB:
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
