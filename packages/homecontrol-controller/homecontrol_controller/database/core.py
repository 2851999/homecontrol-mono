from typing import Optional

from homecontrol_base_api.database.core import DatabaseSession

from homecontrol_controller.database.ac_devices import ACDevicesSession


class ControllerDatabaseSession(DatabaseSession):
    """Handles a controllelr database session."""

    _ac_devices: Optional[ACDevicesSession] = None

    @property
    def ac_devices(self) -> ACDevicesSession:
        if not self._users:
            self._users = ControllerDatabaseSession(self._session)
        return self._users
