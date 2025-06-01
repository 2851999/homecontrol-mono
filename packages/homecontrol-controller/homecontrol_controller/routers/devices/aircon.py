from fastapi import APIRouter, status

from homecontrol_controller.dependencies import ControllerServiceDep
from homecontrol_controller.schemas.ac_devices import ACDevice, ACDevicePost, ACDeviceState

aircon = APIRouter(prefix="/aircon", tags=["Air Conditioning"])


@aircon.post("", summary="Create an AC device", status_code=status.HTTP_201_CREATED)
async def create(ac_device: ACDevicePost, controller_service: ControllerServiceDep) -> ACDevice:
    return await controller_service.devices.aircon.create(ac_device)


@aircon.get(
    "/{device_id}/state", summary="Obtain the current state of an AC device", status_code=status.HTTP_201_CREATED
)
async def get_state(device_id: str, controller_service: ControllerServiceDep) -> ACDeviceState:
    return await controller_service.devices.aircon.get_state(device_id)
