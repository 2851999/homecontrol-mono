from fastapi import APIRouter, status

from homecontrol_controller.dependencies import ControllerServiceDep
from homecontrol_controller.schemas.aircon import ACDevice, ACDevicePost, ACDeviceState, ACDeviceStatePatch

aircon = APIRouter(prefix="/aircon", tags=["Air Conditioning"])


@aircon.post("", summary="Create an AC device", status_code=status.HTTP_201_CREATED)
async def create(ac_device: ACDevicePost, controller_service: ControllerServiceDep) -> ACDevice:
    return await controller_service.devices.aircon.create(ac_device)


@aircon.get("", summary="Get a list of AC devices", status_code=status.HTTP_201_CREATED)
async def get_all(controller_service: ControllerServiceDep) -> list[ACDevice]:
    return await controller_service.devices.aircon.get_all()


@aircon.get("/{device_id}/state", summary="Get the current state of an AC device", status_code=status.HTTP_201_CREATED)
async def get_state(device_id: str, controller_service: ControllerServiceDep) -> ACDeviceState:
    return await controller_service.devices.aircon.get_state(device_id)


@aircon.patch("/{device_id}/state", summary="Change the current state of an AC device")
async def patch_state(
    device_id: str, state_patch: ACDeviceStatePatch, controller_service: ControllerServiceDep
) -> ACDeviceState:
    return await controller_service.devices.aircon.update_state(device_id, state_patch)
