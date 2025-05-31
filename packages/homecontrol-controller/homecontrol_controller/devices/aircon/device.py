import asyncio

from msmart.const import DeviceType
from msmart.device.AC.device import AirConditioner
from msmart.lan import AuthenticationError

from homecontrol_controller.database.models import ACDeviceInDB
from homecontrol_controller.exceptions import DeviceAuthenticationError


class ACDevice:
    """A physical AC device."""

    _info: ACDeviceInDB
    _device: AirConditioner

    def __init__(self, ac_device: ACDeviceInDB):
        """Intialises this AC device given the information stored in the database about it."""

        self._info = ac_device
        self._device = AirConditioner(
            ip=self._info.ip_address,
            device_id=ac_device.identifier,
            port=ac_device.port,
            type=DeviceType.AIR_CONDITIONER,
        )

    async def initialise(self) -> None:
        """Initialises this device ready for controlling it."""

        # Have previously found can be tempermental so retry authentication up to 3 times here
        for retry in range(0, 3):
            try:
                await self._device.authenticate(token=self._info.token, key=self._info.key)
                break
            except AuthenticationError as exc:
                if retry == 2:
                    raise DeviceAuthenticationError(
                        f"Failed to authenticate AC device with name '{self._info.name}'"
                    ) from exc
                else:
                    await asyncio.sleep(1)
        await self._device.get_capabilities()
