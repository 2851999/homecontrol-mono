from fastapi import APIRouter

from homecontrol_controller.dependencies import ControllerServiceDep
from homecontrol_controller.schemas.hue import HueBridgeDeviceDiscoveryInfo

hue = APIRouter(prefix="/hue", tags=["Hue"])


@hue.get("/discover", summary="Discover a list of Hue Bridges")
async def discover_bridges(controller_service: ControllerServiceDep) -> list[HueBridgeDeviceDiscoveryInfo]:
    return await controller_service.devices.hue.discover_bridges()
