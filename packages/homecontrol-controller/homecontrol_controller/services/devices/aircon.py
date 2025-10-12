from pydantic import TypeAdapter

from homecontrol_controller.config import settings
from homecontrol_controller.database.ac_devices import ACDevicesSession
from homecontrol_controller.devices.aircon.discovery import ACDiscovery
from homecontrol_controller.devices.aircon.manager import ACManager
from homecontrol_controller.schemas.aircon import (
    ACDevice,
    ACDeviceDiscoveryInfo,
    ACDevicePost,
    ACDeviceState,
    ACDeviceStatePatch,
)


class ACService:
    """Service that handles AC devices."""

    _session: ACDevicesSession
    _manager: ACManager

    def __init__(self, session: ACDevicesSession, manager: ACManager):
        self._session = session
        self._manager = manager

    async def discover_units(self) -> ACDeviceDiscoveryInfo:
        """Attempts to discover all AC devices that are available on the current network."""

        return await ACDiscovery.discover(settings=settings.midea)

    async def create(self, ac_device: ACDevicePost) -> ACDevice:
        """Creates an AC device.

        :param ac_device: AC device to create.
        :return: Created AC device.
        """

        found_device = await ACDiscovery.authenticate(
            name=ac_device.name, discovery_info=ac_device.discovery_info, settings=settings.midea
        )
        ac_device_out = await self._session.create(found_device)
        await self._manager.add(ac_device=ac_device_out)

        return ACDevice.model_validate(ac_device_out)

    async def get_all(self) -> list[ACDevice]:
        """Returns a list of AC devices.

        :return: List of AC devices.
        """

        return TypeAdapter(list[ACDevice]).validate_python(await self._session.get_all())

    async def get_state(self, device_id: str) -> ACDeviceState:
        """Obtains an AC device's current state.

        :param device_id: ID of the AC device to obtain the current state of.
        :return: The current state of the device.
        """

        return await self._manager.get(device_id).get_state()

    async def update_state(self, device_id: str, state_patch: ACDeviceStatePatch) -> ACDeviceState:
        """Updates an AC device's current state.

        :param device_id: ID of the AC device to change the state of.
        :param state_patch: Change of state to apply to the device.
        :return: The new state of the device.
        """

        return await self._manager.get(device_id).update_state(state_patch)
