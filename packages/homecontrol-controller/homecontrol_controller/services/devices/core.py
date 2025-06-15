from typing import Optional

from homecontrol_controller.database.core import ControllerDatabaseSession
from homecontrol_controller.devices.aircon.manager import ACManager
from homecontrol_controller.devices.hue.manager import HueBridgeManager
from homecontrol_controller.services.devices.aircon import ACService
from homecontrol_controller.services.devices.hue import HueService


class DeviceService:
    """Service that handles devices."""

    _session: ControllerDatabaseSession
    _ac_manager: ACManager
    _hue_bridge_manager: HueBridgeManager

    _aircon: Optional[ACService] = None
    _hue: Optional[HueService] = None

    def __init__(self, session: ControllerDatabaseSession, ac_manager: ACManager, hue_bridge_manager: HueBridgeManager):
        self._session = session
        self._ac_manager = ac_manager
        self._hue_bridge_manager = hue_bridge_manager

    @property
    def aircon(self) -> ACService:
        if not self._aircon:
            self._aircon = ACService(self._session.ac_devices, self._ac_manager)
        return self._aircon

    @property
    def hue(self) -> HueService:
        if not self._hue:
            self._hue = HueService(self._session.hue_bridge_devices, self._hue_bridge_manager)
        return self._hue
