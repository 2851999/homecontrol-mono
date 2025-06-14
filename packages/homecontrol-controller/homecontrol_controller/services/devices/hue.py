from homecontrol_controller.config import settings
from homecontrol_controller.database.hue_bridge_devices import HueBridgeDevicesSession
from homecontrol_controller.devices.hue.discovery import HueBridgeDiscovery
from homecontrol_controller.devices.hue.manager import HueBridgeManager
from homecontrol_controller.schemas.hue import HueBridgeDevice, HueBridgeDeviceDiscoveryInfo, HueBridgeDevicePost


class HueService:
    """Service that handles Hue devices."""

    _session: HueBridgeDevicesSession
    _bridge_manager: HueBridgeManager

    def __init__(self, session: HueBridgeDevicesSession, bridge_manager: HueBridgeManager):
        self._session = session
        self._bridge_manager = bridge_manager

    async def discover_bridges(self) -> HueBridgeDeviceDiscoveryInfo:
        """Attempts to discover all Hue Bridges that are available on the current network."""

        return await HueBridgeDiscovery.discover(use_mDNS=settings.hue.use_mDNS_discovery)

    async def create(self, hue_bridge_device: HueBridgeDevicePost) -> HueBridgeDevice:
        """Creates a Hue Bridge device

        :param hue_bridge_device: Hue Bridge device to create.
        :returns: Created Hue Bridge device.
        """

        authenticated_device = await HueBridgeDiscovery.authenticate(
            name=hue_bridge_device.name, discovery_info=hue_bridge_device.discovery_info, settings=settings.hue
        )
        hue_bridge_device_out = await self._session.create(authenticated_device)
        return HueBridgeDevice.model_validate(hue_bridge_device_out)
