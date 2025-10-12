from pydantic import TypeAdapter

from homecontrol_controller.database.models import RoomInDB
from homecontrol_controller.database.rooms import RoomsSession
from homecontrol_controller.schemas.rooms import Room, RoomPost


class RoomService:
    """Service that handles Rooms."""

    _session: RoomsSession

    def __init__(self, session: RoomsSession):
        self._session = session

    async def create(self, room: RoomPost) -> Room:
        """Creayes a Room.

        :param room: Room to create.
        :return: Created Room.
        """

        room_in = RoomInDB(name=room.name, controllers=[controller.model_dump() for controller in room.controllers])
        room_out = await self._session.create(room_in)
        return Room.model_validate(room_out)

    async def get_all(self) -> list[Room]:
        """Returns a list of Rooms.

        :return: List of rooms.
        """

        return TypeAdapter(list[Room]).validate_python(await self._session.get_all())
