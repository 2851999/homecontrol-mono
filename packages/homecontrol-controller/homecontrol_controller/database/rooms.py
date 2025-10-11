from uuid import UUID

from homecontrol_base_api.database.core import DatabaseSession
from homecontrol_base_api.exceptions import RecordNotFoundError
from sqlalchemy import delete
from sqlalchemy import exc as sqlalchemy_exc
from sqlalchemy import select

from homecontrol_controller.database.models import RoomInDB


class RoomsSession(DatabaseSession):
    """Handles Rooms in the database."""

    async def create(self, room: RoomInDB) -> RoomInDB:
        """Creates a Room in the database.

        :param room: Room to create.
        :returnes: Created room.
        """

        self._session.add(room)
        await self._session.commit()
        await self._session.refresh()
        return room

    async def get(self, room_id: str) -> RoomInDB:
        """Returns a Room from the database given its ID.

        :param room_id: ID of the room to get.
        :returns: The room.
        :raises RecordNotFoundError: If the room with the given ID is not found in the database.
        """

        try:
            return (await self._session.execute(select(RoomInDB).where(RoomInDB.id == UUID(room_id)))).scalar_one()
        except (sqlalchemy_exc.NoResultFound, ValueError) as exc:
            raise RecordNotFoundError(f"No room found with the ID '{room_id}'") from exc

    async def get_all(self) -> list[RoomInDB]:
        """Returns a list of all the Rooms from the databse.

        :returns: List of rooms.
        """

        return (await self._session.execute(select(RoomInDB))).scalars().all()

    async def update(self, room: RoomInDB) -> RoomInDB:
        """Updates a room by commiting any changes to the database.

        :param room: Room to update.
        :returns: The room.
        """

        # TODO: Check if this enough, before had to use mutable_json_type(dbtype=JSON, nested=True) for the json data to update
        # might be alternative way to force without extra library

        await self._session.commit()
        await self._session.refresh(room)
        return room

    async def delete(self, room_id: str) -> None:
        """Deletes a room from the databse given its ID.

        :param room_id: ID of the room to delete.
        :raises RecordNotFoundError: If the room with the given ID is not found in the database.
        """

        try:
            result = await self._session.execute(delete(RoomInDB).where(RoomInDB.id == UUID(room_id)))
        except ValueError as exc:
            raise RecordNotFoundError(f"No room found with the ID '{room_id}'") from exc

        if result.rowcount == 0:
            raise RecordNotFoundError(f"No room found with the ID '{room_id}'")

        await self._session.commit()
