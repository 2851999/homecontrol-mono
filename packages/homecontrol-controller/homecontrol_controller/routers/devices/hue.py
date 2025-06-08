from fastapi import APIRouter, status

from homecontrol_controller.dependencies import ControllerServiceDep
from homecontrol_controller.schemas.hue import HueBridgeDevice, HueBridgeDeviceDiscoveryInfo, HueBridgeDevicePost

hue = APIRouter(prefix="/hue", tags=["Hue"])


@hue.get("/discover", summary="Discover a list of Hue Bridges")
async def discover_bridges(controller_service: ControllerServiceDep) -> list[HueBridgeDeviceDiscoveryInfo]:
    return await controller_service.devices.hue.discover_bridges()


@hue.post("", summary="Create a Hue Bridge device", status_code=status.HTTP_201_CREATED)
async def create(hue_bridge_device: HueBridgeDevicePost, controller_service: ControllerServiceDep) -> HueBridgeDevice:
    return await controller_service.devices.hue.create(hue_bridge_device)
