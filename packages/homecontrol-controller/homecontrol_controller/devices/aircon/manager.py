from homecontrol_controller.database.models import ACDeviceInDB
from homecontrol_controller.devices.aircon.device import ACDevice
from homecontrol_controller.exceptions import DeviceNotFoundError


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
