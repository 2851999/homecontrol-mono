from typing import Optional

from homecontrol_base_api.database.core import DatabaseSession

from homecontrol_controller.database.ac_devices import ACDevicesSession
from homecontrol_controller.database.hue_bridge_devices import HueBridgeDevicesSession


class ControllerDatabaseSession(DatabaseSession):
    """Handles a controllelr database session."""

    _ac_devices: Optional[ACDevicesSession] = None
    _hue_bridge_devices: Optional[HueBridgeDevicesSession] = None

    @property
    def ac_devices(self) -> ACDevicesSession:
        if not self._ac_devices:
            self._ac_devices = ACDevicesSession(self._session)
        return self._ac_devices

    @property
    def hue_bridge_devices(self) -> HueBridgeDevicesSession:
        if not self._hue_bridge_devices:
            self._hue_bridge_devices = HueBridgeDevicesSession(self._session)
        return self._hue_bridge_devices
