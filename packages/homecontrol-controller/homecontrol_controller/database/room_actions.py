from uuid import UUID

from homecontrol_base_api.database.core import DatabaseSession
from homecontrol_base_api.exceptions import RecordNotFoundError
from sqlalchemy import delete, select
from sqlalchemy import exc as sqlalchemy_exc

from homecontrol_controller.database.models import RoomActionInDB


class RoomActionsSession(DatabaseSession):
    """Handles room actions in the database."""

    async def create(self, room_action: RoomActionInDB) -> RoomActionInDB:
        """Creates a room action in the database.

        :param room: Room action to create.
        :returns: Created room action.
        """

        self._session.add(room_action)
        await self._session.commit()
        await self._session.refresh(room_action)
        return room_action

    async def get(self, room_action_id: str) -> RoomActionInDB:
        """Returns a room action from the database given its ID.

        :param room_action_id: ID of the room action to get.
        :return: The room action.
        :raises RecordNotFoundError: If the room action with the given ID is not found in the database.
        """

        try:
            return (
                await self._session.execute(select(RoomActionInDB).where(RoomActionInDB.id == UUID(room_action_id)))
            ).scalar_one()
        except (sqlalchemy_exc.NoResultFound, ValueError) as exc:
            raise RecordNotFoundError(f"No room action found with the ID '{room_action_id}'") from exc

    async def get_all(self) -> list[RoomActionInDB]:
        """Returns a list of all the room actions from the databse.

        :return: List of room actions.
        """

        return (await self._session.execute(select(RoomActionInDB))).scalars().all()

    async def update(self, room: RoomActionInDB) -> RoomActionInDB:
        """Updates a room action by commiting any changes to the database.

        :param room_action: Room actions to update.
        :return: The room action.
        """

        # TODO: Check if this enough, before had to use mutable_json_type(dbtype=JSON, nested=True) for the json data to update
        # might be alternative way to force without extra library

        await self._session.commit()
        await self._session.refresh(room)
        return room

    async def delete(self, room_action_id: str) -> None:
        """Deletes a room action from the databse given its ID.

        :param room_action_id: ID of the room action to delete.
        :raises RecordNotFoundError: If the room action with the given ID is not found in the database.
        """

        try:
            result = await self._session.execute(
                delete(RoomActionInDB).where(RoomActionInDB.id == UUID(room_action_id))
            )
        except ValueError as exc:
            raise RecordNotFoundError(f"No room action found with the ID '{room_action_id}'") from exc

        if result.rowcount == 0:
            raise RecordNotFoundError(f"No room action found with the ID '{room_action_id}'")

        await self._session.commit()
