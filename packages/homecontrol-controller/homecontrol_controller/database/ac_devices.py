from uuid import UUID

from homecontrol_base_api.database.core import DatabaseSession
from homecontrol_base_api.exceptions import RecordNotFoundError
from sqlalchemy import delete, select

from homecontrol_controller.database.models import ACDeviceInDB


class ACDevicesSession(DatabaseSession):
    """Handles AC device's in the database"""

    async def create(self, ac_device: ACDeviceInDB) -> ACDeviceInDB:
        """Creates an AC device in the database.

        :param ac_device: AC device to create.
        :returns: Created AC device.
        """

        self._session.add(ac_device)
        await self._session.commit()
        await self._session.refresh(ac_device)
        return ac_device

    async def get(self, device_id: str) -> ACDeviceInDB:
        """Returns an AC device from the database given its ID.

        :param device_id: ID of the AC device to get.
        :returns: The AC device.
        :raises RecordNotFoundError: If the AC device with the given ID is not found in the database.
        """

        try:
            return (
                await self._session.execute(select(ACDeviceInDB).where(ACDeviceInDB.id == UUID(device_id)))
            ).scalar_one()
        except (exc.NoResultFound, ValueError) as exc:
            raise RecordNotFoundError(f"No AC device found with the ID '{device_id}'") from exc

    async def get_all(self) -> list[ACDeviceInDB]:
        """Returns a list of all AC devices from the database.

        :returns: List of AC devices.
        """

        return (await self._session.execute(select(ACDeviceInDB))).scalars().all()

    async def update(self, ac_device: ACDeviceInDB) -> ACDeviceInDB:
        """Updates an AC device by commiting any changes to the database.

        :param ac_device: AC device to update.
        :returns: The AC device.
        """

        await self._session.commit()
        await self._session.refresh(ac_device)
        return ac_device

    async def delete(self, device_id: str) -> None:
        """Deletes an AC device from the database given its ID.

        :param device_id: ID of the AC device to delete.
        :raises RecordNotFoundError: If the AC device with the given ID is not found in the database.
        """

        try:
            result = await self._session.execute(delete(ACDeviceInDB).where(ACDeviceInDB.id == UUID(device_id)))
        except ValueError as exc:
            raise RecordNotFoundError(f"No AC device found with the ID '{device_id}'") from exc

        if result.rowcount == 0:
            raise RecordNotFoundError(f"No AC device found with the ID '{device_id}'")

        await self._session.commit()
