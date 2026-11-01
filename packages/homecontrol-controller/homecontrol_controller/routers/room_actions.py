from fastapi import APIRouter, status

from homecontrol_controller.dependencies import ControllerServiceDep
from homecontrol_controller.schemas.room_actions import RoomAction, RoomActionPost

room_actions = APIRouter(prefix="/room-actions", tags=["Room Actions"])


@room_actions.post("", summary="Create a room action", status_code=status.HTTP_201_CREATED)
async def create(room: RoomActionPost, controller_service: ControllerServiceDep) -> RoomAction:
    return await controller_service.room_actions.create(room)


@room_actions.get("", summary="Get a list of room actions")
async def get_all(controller_service: ControllerServiceDep) -> list[RoomAction]:
    return await controller_service.room_actions.get_all()


@room_actions.post("/{room_action_id}", summary="Create a room action", status_code=status.HTTP_204_NO_CONTENT)
async def execute(room_action_id: str, controller_service: ControllerServiceDep) -> None:
    return await controller_service.room_actions.execute(room_action_id)
