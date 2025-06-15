from contextlib import asynccontextmanager
from typing import AsyncGenerator

from homecontrol_controller.database.models import HueBridgeDeviceInDB
from homecontrol_controller.devices.hue.session import HueBridgeSession, create_hue_bridge_session


class HueBridgeDevice:
    """A physical Hue Bridge device."""

    _info: HueBridgeDeviceInDB

    def __init__(self, hue_bridge_device: HueBridgeDeviceInDB):
        """Initialises this Hue Bridge device given the information stored in the database about it."""

        self._info = hue_bridge_device

    @asynccontextmanager
    async def connect(self) -> AsyncGenerator[HueBridgeSession, None]:
        """Connect to this Hue Bridge and return a session to interact with it."""

        async with create_hue_bridge_session(self._info) as session:
            yield session
