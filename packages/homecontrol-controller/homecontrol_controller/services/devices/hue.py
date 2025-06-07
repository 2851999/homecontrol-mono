from homecontrol_controller.config import settings
from homecontrol_controller.devices.hue.discovery import discover_hue_bridges
from homecontrol_controller.schemas.hue import HueBridgeDiscoveryInfo


class HueService:
    """Servuce that handles Hue devices."""

    async def discover_bridges(self) -> HueBridgeDiscoveryInfo:
        """Attempts to discover all Hue Bridges that are available on the current network."""

        return await discover_hue_bridges(use_mDNS=settings.hue.use_mDNS_discovery)
