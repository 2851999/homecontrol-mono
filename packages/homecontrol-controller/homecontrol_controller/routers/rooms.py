from fastapi import APIRouter, status

from homecontrol_controller.dependencies import ControllerServiceDep
from homecontrol_controller.schemas.rooms import Room, RoomPost

rooms = APIRouter(prefix="/rooms", tags=["Rooms"])


@rooms.post("", summary="Create a Room", status_code=status.HTTP_201_CREATED)
async def create(room: RoomPost, controller_service: ControllerServiceDep) -> Room:
    return await controller_service.rooms.create(room)


@rooms.get("", summary="Get a list of Rooms")
async def get_all(controller_service: ControllerServiceDep) -> list[Room]:
    return await controller_service.rooms.get_all()
