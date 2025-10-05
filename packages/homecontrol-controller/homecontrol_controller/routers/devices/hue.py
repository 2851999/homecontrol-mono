from fastapi import APIRouter, status

from homecontrol_controller.dependencies import ControllerServiceDep
from homecontrol_controller.schemas.hue import (
    HueBridgeDevice,
    HueBridgeDeviceDiscoveryInfo,
    HueBridgeDevicePost,
    HueRoom,
    HueRoomState,
    HueRoomStatePatch,
)

hue = APIRouter(prefix="/hue", tags=["Hue"])


@hue.get("/discover", summary="Discover a list of Hue Bridges")
async def discover_bridges(controller_service: ControllerServiceDep) -> list[HueBridgeDeviceDiscoveryInfo]:
    return await controller_service.devices.hue.discover_bridges()


@hue.post("", summary="Create a Hue Bridge device", status_code=status.HTTP_201_CREATED)
async def create(hue_bridge_device: HueBridgeDevicePost, controller_service: ControllerServiceDep) -> HueBridgeDevice:
    return await controller_service.devices.hue.create(hue_bridge_device)


@hue.get("", summary="Get a list of Hue Bridge devices")
async def get_all(controller_service: ControllerServiceDep) -> list[HueBridgeDevice]:
    return await controller_service.devices.hue.get_all_bridges()


@hue.get("/{bridge_id}/rooms", summary="Get a list rooms managed by a Hue Bridge")
async def get_all_rooms(bridge_id: str, controller_service: ControllerServiceDep) -> list[HueRoom]:
    bridge = await controller_service.devices.hue.get_bridge_device(bridge_id)
    async with bridge.connect() as session:
        return await session.rooms.get_all()


@hue.get("/{bridge_id}/rooms/{room_id}", summary="Get a room managed by a Hue Bridge")
async def get_room(bridge_id: str, room_id: str, controller_service: ControllerServiceDep) -> HueRoom:
    bridge = await controller_service.devices.hue.get_bridge_device(bridge_id)
    async with bridge.connect() as session:
        return await session.rooms.get(room_id)


@hue.get("/{bridge_id}/rooms/{room_id}/state", summary="Get a room state of a room managed by a Hue Bridge")
async def get_room_state(bridge_id: str, room_id: str, controller_service: ControllerServiceDep) -> HueRoomState:
    bridge = await controller_service.devices.hue.get_bridge_device(bridge_id)
    async with bridge.connect() as session:
        return await session.rooms.get_state(room_id)


@hue.patch("/{bridge_id}/rooms/{room_id}/state", summary="Change the state of a room managed by a Hue Bridge")
async def patch_room_state(
    bridge_id: str, room_id: str, state_patch: HueRoomStatePatch, controller_service: ControllerServiceDep
) -> HueRoomState:
    bridge = await controller_service.devices.hue.get_bridge_device(bridge_id)
    async with bridge.connect() as session:
        return await session.rooms.update_state(room_id, state_patch)
