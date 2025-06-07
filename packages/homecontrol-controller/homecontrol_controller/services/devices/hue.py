from homecontrol_controller.config import settings
from homecontrol_controller.devices.hue.discovery import HueBridgeDiscovery
from homecontrol_controller.schemas.hue import HueBridgeDeviceDiscoveryInfo


class HueService:
    """Service that handles Hue devices."""

    async def discover_bridges(self) -> HueBridgeDeviceDiscoveryInfo:
        """Attempts to discover all Hue Bridges that are available on the current network."""

        return await HueBridgeDiscovery.discover(use_mDNS=settings.hue.use_mDNS_discovery)
