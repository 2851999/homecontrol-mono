from homecontrol_controller.config import settings
from homecontrol_controller.database.ac_devices import ACDevicesSession
from homecontrol_controller.devices.aircon.manager import ACManager
from homecontrol_controller.schemas.ac_devices import ACDevice, ACDevicePost, ACDeviceState


class ACService:
    """Service that handles AC devcies."""

    _session: ACDevicesSession
    _manager: ACManager

    def __init__(self, session: ACDevicesSession, manager: ACManager):
        self._session = session
        self._manager = manager

    async def create(self, ac_device: ACDevicePost) -> ACDevice:
        """Creates an AC device.

        :param ac_device: AC device to create.
        :returns: Created AC device.
        """

        found_device = await ACManager.discover(
            name=ac_device.name, ip_address=ac_device.ip_address, settings=settings.midea
        )
        ac_device_out = await self._session.create(found_device)
        await self._manager.add(ac_device=ac_device_out)

        return ACDevice.model_validate(ac_device_out)

    async def get_state(self, device_id: str) -> ACDeviceState:
        """Obtains an AC device's current state.

        :param device_id: ID of the AC device to obtain the current state of.
        :return: The current state of the device.
        """

        return await self._manager.get(device_id).get_state()
