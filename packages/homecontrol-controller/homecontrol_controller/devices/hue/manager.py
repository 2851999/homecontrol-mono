from homecontrol_controller.database.models import HueBridgeDeviceInDB
from homecontrol_controller.devices.hue.bridge import HueBridgeDevice
from homecontrol_controller.exceptions import DeviceNotFoundError


class HueBridgeManager:
    """Manages a set of Hue Bridge devices."""

    _devices: dict[str, HueBridgeDevice]

    def __init__(self):
        self._devices = {}

    def add(self, hue_bridge_device: HueBridgeDeviceInDB) -> HueBridgeDevice:
        """Adds a Hue Bridge device to this manager.

        :param hue_bridge_device: Database model of the device to add.
        :returns: The Hue Bridge device.
        """
        device = HueBridgeDevice(hue_bridge_device)
        self._devices[str(hue_bridge_device.id)] = device
        return device

    def add_all(self, hue_bridge_devices: list[HueBridgeDeviceInDB]) -> None:
        """Loads a list of Hue Bridge devices, adding each to this manager.

        :param hue_bridge_devices: List of database models of the devices to add.
        """

        for hue_bridge_device in hue_bridge_devices:
            self.add(hue_bridge_device)

    def get(self, device_id: str) -> HueBridgeDevice:
        """Returns a Hue Bridge device given its ID.

        :param device_id: ID of the Hue Bridge device to get.
        :raises: DeviceNotFoundError: If the Hue Bridge device with the given ID is not found.
        """

        device = self._devices.get(device_id)
        if device is None:
            raise DeviceNotFoundError(f"Hue Bridge device with ID '{device_id}' was not found")
        return device
