import asyncio
from typing import Optional

from homecontrol_controller.devices.hue.api.schemas import RoomGet
from homecontrol_controller.devices.hue.api.session import HueBridgeAPISession
from homecontrol_controller.schemas.hue import HueRoom, HueRoomLight


class HueRoomService:
    """Service that handles rooms in Hue."""

    _session: HueBridgeAPISession

    def __init__(self, session: HueBridgeAPISession):
        """Intiialise this service for controlling a room's Hue devices.

        :param session: API session for the Hue bridge.
        """
        self._session = session

    async def _get(self, room: RoomGet) -> HueRoom:
        """Constructs a HueRoom by performing the required gets to a Hue Bridge."""

        # Attempt to find a grouped light service
        grouped_light_id: Optional[str] = None
        for service in room.services:
            if service.rtype == "grouped_light":
                grouped_light_id = service.rid

        # Locate all lights
        lights: list[HueRoomLight] = []
        for child in room.children:
            if child.rtype == "device":
                device = await self._session.get_device(child.rid)
                for service in device.services:
                    if service.rtype == "light":
                        lights.append(HueRoomLight(id=child.rid, name=device.metadata.name))
                        break
        return HueRoom(id=room.id, name=room.metadata.name, grouped_light_id=grouped_light_id, lights=lights)

    async def get_all(self) -> list[HueRoom]:
        """Returns a list of all rooms managed by the Hue Bridge.

        :returns: List of all rooms.
        """

        rooms = await self._session.get_rooms()
        return await asyncio.gather(*(self._get(room) for room in rooms))

    async def get(self, room_id: str) -> HueRoom:
        """Obtains a room managed by the Hue Bridge given its ID.

        :param room_id: ID of the room to obtain.
        :retrurn: The obtained room.
        """

        return await self._get(await self._session.get_room(room_id))
