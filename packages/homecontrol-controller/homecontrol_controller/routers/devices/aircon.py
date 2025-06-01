from fastapi import APIRouter, status

from homecontrol_controller.dependencies import ControllerServiceDep
from homecontrol_controller.schemas.ac_devices import ACDevice, ACDevicePost

aircon = APIRouter(prefix="/aircon", tags=["Air Conditioning"])


@aircon.post("", summary="Create an AC device", status_code=status.HTTP_201_CREATED)
async def create(ac_device: ACDevicePost, controller_service: ControllerServiceDep) -> ACDevice:
    return await controller_service.devices.aircon.create(ac_device)
