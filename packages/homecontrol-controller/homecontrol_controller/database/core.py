from homecontrol_base_api.database.core import DatabaseSession

from homecontrol_controller.database.ac_devices import ACDevicesSession
from homecontrol_controller.database.hue_bridge_devices import HueBridgeDevicesSession
from homecontrol_controller.database.room_actions import RoomActionsSession
from homecontrol_controller.database.rooms import RoomsSession


class ControllerDatabaseSession(DatabaseSession):
    """Handles a controller database session."""

    _ac_devices: ACDevicesSession | None = None
    _hue_bridge_devices: HueBridgeDevicesSession | None = None
    _rooms: RoomsSession | None = None
    _room_actions: RoomActionsSession | None = None

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

    @property
    def rooms(self) -> RoomsSession:
        if not self._rooms:
            self._rooms = RoomsSession(self._session)
        return self._rooms

    @property
    def room_actions(self) -> RoomActionsSession:
        if not self._room_actions:
            self._room_actions = RoomActionsSession(self._session)
        return self._room_actions
