from typing import Optional

from homecontrol_controller.database.core import ControllerDatabaseSession
from homecontrol_controller.devices.aircon.manager import ACManager
from homecontrol_controller.services.devices.ac_service import ACService


class DeviceService:
    """Service that handles devices."""

    _session: ControllerDatabaseSession
    _ac_manager: ACManager

    _aircon: Optional[ACService] = None

    def __init__(self, session: ControllerDatabaseSession, ac_manager: ACManager):
        self._session = session
        self._ac_manager = ac_manager

    @property
    def aircon(self) -> ACService:
        if not self._aircon:
            self._aircon = ACService(self._session.ac_devices, self._ac_manager)
        return self._aircon
