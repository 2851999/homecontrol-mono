from uuid import UUID

from homecontrol_base_api.database.core import DatabaseSession
from homecontrol_base_api.exceptions import RecordNotFoundError
from sqlalchemy import delete, select

from homecontrol_controller.database.models import HueBridgeDeviceInDB


class HueBridgeDevicesSession(DatabaseSession):
    """Handles Hue Bridge device's in the database"""

    async def create(self, hue_bridge_device: HueBridgeDeviceInDB) -> HueBridgeDeviceInDB:
        """Creates an Hue Bridge device in the database.

        :param hue_bridge_device: Hue Bridg device to create.
        :returns: Created Hue Bridg device.
        """

        self._session.add(hue_bridge_device)
        await self._session.commit()
        await self._session.refresh(hue_bridge_device)
        return hue_bridge_device

    async def get(self, device_id: str) -> HueBridgeDeviceInDB:
        """Returns an Hue Bridge device from the database given its ID.

        :param device_id: ID of the Hue Bridge device to get.
        :returns: The Hue Bridge device.
        :raises RecordNotFoundError: If the Hue Bridge device with the given ID is not found in the database.
        """

        try:
            return (
                await self._session.execute(
                    select(HueBridgeDeviceInDB).where(HueBridgeDeviceInDB.id == UUID(device_id))
                )
            ).scalar_one()
        except (exc.NoResultFound, ValueError) as exc:
            raise RecordNotFoundError(f"No Hue Bridge device found with the ID '{device_id}'") from exc

    async def get_all(self) -> list[HueBridgeDeviceInDB]:
        """Returns a list of all Hue Bridge devices from the database.

        :returns: List of Hue Bridge devices.
        """

        return (await self._session.execute(select(HueBridgeDeviceInDB))).scalars().all()

    async def update(self, hue_bridge_device: HueBridgeDeviceInDB) -> HueBridgeDeviceInDB:
        """Updates a Hue Bridge device by commiting any changes to the database.

        :param hue_bridge_device: Hue Bridge device to update.
        :returns: The Hue Bridge device.
        """

        await self._session.commit()
        await self._session.refresh(hue_bridge_device)
        return hue_bridge_device

    async def delete(self, device_id: str) -> None:
        """Deletes a Hue Bridge device from the database given its ID.

        :param device_id: ID of the Hue Bridge device to delete.
        :raises RecordNotFoundError: If the Hue Bridge device with the given ID is not found in the database.
        """

        try:
            result = await self._session.execute(
                delete(HueBridgeDeviceInDB).where(HueBridgeDeviceInDB.id == UUID(device_id))
            )
        except ValueError as exc:
            raise RecordNotFoundError(f"No Hue Bridge device found with the ID '{device_id}'") from exc

        if result.rowcount == 0:
            raise RecordNotFoundError(f"No Hue Bridge device found with the ID '{device_id}'")

        await self._session.commit()
