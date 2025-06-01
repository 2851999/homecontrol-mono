from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from homecontrol_base_api.database.core import get_database

from homecontrol_controller.config import settings
from homecontrol_controller.database.core import ControllerDatabaseSession
from homecontrol_controller.devices.aircon.manager import ACManager
from homecontrol_controller.services.devices.core import DeviceService


class ControllerService:
    """Service that handles the control of devices."""

    _session: ControllerDatabaseSession
    _ac_manager: ACManager

    _devices: Optional[DeviceService] = None

    def __init__(self, session: ControllerDatabaseSession, ac_manager: ACManager):
        self._session = session
        self._ac_manager = ac_manager

    @property
    def devices(self) -> DeviceService:
        if not self._devices:
            self._devices = DeviceService(self._session, self._ac_manager)
        return self._devices


@asynccontextmanager
async def create_controller_service(ac_manager: ACManager) -> AsyncGenerator[ControllerService, None]:
    """Creates an instance of the controller service."""

    async with get_database(ControllerDatabaseSession, settings.database) as database:
        async with database.start_session() as session:
            yield ControllerService(session, ac_manager)
