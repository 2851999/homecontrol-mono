from pydantic import TypeAdapter

from homecontrol_controller.database.models import RoomActionInDB
from homecontrol_controller.database.room_actions import RoomActionsSession
from homecontrol_controller.devices.hue.api.schemas import RecallPut, ScenePut
from homecontrol_controller.schemas.room_actions import RoomAction, RoomActionPost, TaskType
from homecontrol_controller.services.devices.core import DeviceService


class RoomActionService:
    """Service that handles room actions."""

    _session: RoomActionsSession
    _device_service: DeviceService

    def __init__(self, session: RoomActionsSession, device_service: DeviceService):
        self._session = session
        self._device_service = device_service

    async def create(self, room_action: RoomActionPost) -> RoomAction:
        """Creates a room action.

        :param room_action: Room action to create.
        :return: Created room action.
        """

        room_in = RoomActionInDB(
            name=room_action.name,
            room_id=room_action.room_id,
            icon=room_action.icon,
            tasks=[task.model_dump() for task in room_action.tasks],
        )
        room_out = await self._session.create(room_in)
        return RoomAction.model_validate(room_out)

    async def get(self, room_action_id: str) -> RoomAction:
        """Returns a room action.

        :param room_action_id: ID of the room action to get.
        """
        return RoomAction.model_validate(await self._session.get(room_action_id))

    async def get_all(self) -> list[RoomAction]:
        """Returns a list of room actions.

        :return: List of room actions.
        """

        return TypeAdapter(list[RoomAction]).validate_python(await self._session.get_all())

    async def execute(self, action_id: str) -> None:
        """Executes a room action.

        :param action_id: ID of the room action to execute.
        """
        action = await self.get(action_id)
        for task in action.tasks:
            match task.type:
                case TaskType.AC_STATE:
                    await self._device_service.aircon.update_state(task.device_id, task.state)
                case TaskType.HUE_SCENE:
                    bridge = await self._device_service.hue.get_bridge_device(task.bridge_id)
                    async with bridge.connect() as session:
                        await session.api.put_scene(task.scene_id, ScenePut(recall=RecallPut(action="active")))
