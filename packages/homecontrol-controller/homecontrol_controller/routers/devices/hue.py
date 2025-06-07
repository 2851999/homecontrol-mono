from fastapi import APIRouter

from homecontrol_controller.dependencies import ControllerServiceDep
from homecontrol_controller.schemas.hue import HueBridgeDiscoveryInfo

hue = APIRouter(prefix="/hue", tags=["Hue"])


@hue.get("/discover", summary="Discover a list of Hue Bridge devices")
async def discover_bridges(controller_service: ControllerServiceDep) -> list[HueBridgeDiscoveryInfo]:
    return await controller_service.devices.hue.discover_bridges()
