import asyncio

from msmart.cloud import CloudError
from msmart.const import DeviceType
from msmart.device.AC.device import AirConditioner
from msmart.lan import AuthenticationError

from homecontrol_controller.database.models import ACDeviceInDB
from homecontrol_controller.exceptions import DeviceAuthenticationError, DeviceConnectionError, DeviceInvalidStateError
from homecontrol_controller.schemas.aircon import ACDeviceState, ACDeviceStatePatch


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

        # Have previously found can be temperamental so retry authentication up to 3 times here
        for retry in range(0, 3):
            try:
                await self._device.authenticate(token=self._info.token, key=self._info.key)
                break
            except (AuthenticationError, CloudError) as exc:
                if retry == 2:
                    raise DeviceAuthenticationError(
                        f"Failed to authenticate AC device with name '{self._info.name}'"
                    ) from exc
                else:
                    await asyncio.sleep(1)
        await self._device.get_capabilities()

    async def _refresh_state(self):
        """Attempts to refresh the device state."""

        # Have previously found can be temperamental so retry if appears wrong
        for retry in range(0, 3):
            await self._device.refresh()
            if self._device.indoor_temperature is None:
                if retry == 2:
                    raise DeviceConnectionError(
                        f"Failed to refresh the state of an AC device with name '{self._info.name}'"
                    )
            else:
                break

    def _get_current_state(self) -> ACDeviceState:
        """Returns the current device state."""

        return ACDeviceState(
            power=self._device.power_state,
            target_temperature=self._device.target_temperature,
            operational_mode=self._device.operational_mode,
            fan_speed=self._device.fan_speed,
            swing_mode=self._device.swing_mode,
            eco_mode=self._device.eco,
            turbo_mode=self._device.turbo,
            rate=self._device.rate_select,
            fahrenheit=self._device.fahrenheit,
            indoor_temperature=self._device.indoor_temperature,
            outdoor_temperature=self._device.outdoor_temperature,
            display_on=self._device.display_on if self._device.power_state else False,
        )

    async def get_state(self) -> ACDeviceState:
        """Obtains the AC device's current state.

        :returns: The current state of the AC device.
        """

        await self._refresh_state()

        # Have previously found can be temperamental, returning 0 even when its not actually accurate, so retry if it appears to have occurred,
        # but if it happens again assume its accurate
        if self._device.indoor_temperature == 0 and self._device.outdoor_temperature == 0:
            await self._refresh_state()

        return self._get_current_state()

    async def update_state(self, state_patch: ACDeviceStatePatch) -> ACDeviceState:
        """Applies a specific change of state to the AC device.

        :param state_patch: Change of state to apply to the device.
        :returns: The current state of the AC device.
        :raises ACInvalidStateError: If the requested state is invalid.
        """

        # Obtaint the current state to patch
        current_state = await self.get_state()
        updated_state = ACDeviceState(**{**current_state.model_dump(), **state_patch.model_dump(exclude_unset=True)})

        # Check the new state is valid
        if state_patch.target_temperature is not None and not 16 <= updated_state.target_temperature <= 30:
            raise DeviceInvalidStateError(
                f"target_temperature of {state_patch.target_temperature} must be between 16 and 30"
            )

        if (
            state_patch.eco_mode is not None
            or state_patch.turbo_mode is not None
            and updated_state.eco_mode
            and updated_state.turbo_mode
        ):
            raise DeviceInvalidStateError(f"Cannot have both 'eco_mode' and 'turbo_mode' True at the same time")

        # Assign the state and figure out if the display should be toggled
        toggle_display = False

        if state_patch.power is not None:
            self._device.power_state = state_patch.power
        if state_patch.target_temperature is not None:
            self._device.target_temperature = state_patch.target_temperature
        if state_patch.operational_mode is not None:
            self._device.operational_mode = state_patch.operational_mode
        if state_patch.fan_speed is not None:
            self._device.fan_speed = state_patch.fan_speed
        if state_patch.swing_mode is not None:
            self._device.swing_mode = state_patch.swing_mode
        if state_patch.eco_mode is not None:
            self._device.eco = state_patch.eco_mode
        if state_patch.turbo_mode is not None:
            self._device.turbo = state_patch.turbo_mode
        if state_patch.rate is not None:
            self._device.rate_select = state_patch.rate
        if state_patch.fahrenheit is not None:
            self._device.fahrenheit = state_patch.fahrenheit
        if state_patch.display_on is not None and current_state.display_on != updated_state.display_on:
            toggle_display = True
        if state_patch.beep is not None:
            self._device.beep = state_patch.beep

        # Have previously found can be temperamental so retry the apply up to 3 times here
        for retry in range(0, 3):
            try:
                # Apply the state and toggle the display if needed
                await self._device.apply()
                if toggle_display:
                    await self._device.toggle_display()
                break
            except UnboundLocalError as exc:
                if retry == 2:
                    raise DeviceAuthenticationError(
                        f"An error occurred while attempting to apply the state of an AC device with name '{self._info.name}'"
                    ) from exc

        return self._get_current_state()
