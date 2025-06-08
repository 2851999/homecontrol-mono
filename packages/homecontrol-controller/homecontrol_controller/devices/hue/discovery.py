import asyncio

import httpx
from pydantic import TypeAdapter
from zeroconf import ServiceStateChange, Zeroconf
from zeroconf.asyncio import AsyncServiceBrowser, AsyncServiceInfo, AsyncZeroconf

from homecontrol_controller.config import HueSettings
from homecontrol_controller.database.models import HueBridgeDeviceInDB
from homecontrol_controller.devices.hue.session import create_hue_bridge_session
from homecontrol_controller.exceptions import (
    DeviceAuthenticationError,
    DeviceDiscoveryError,
    HueBridgeButtonNotPressedError,
)
from homecontrol_controller.schemas.hue import HueBridgeDeviceDiscoveryInfo

DISCOVER_URL = "https://discovery.meethue.com/"


class HueBridgeDiscoveryListener:
    """Listener for Hue Bridges"""

    _found_devices: list[HueBridgeDeviceDiscoveryInfo]

    def __init__(self, **args):
        super().__init__(**args)
        self._found_devices = []

    async def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        """Called when service is first discovered"""

        info = AsyncServiceInfo(type_, name)
        await info.async_request(zc, 3000)
        self._found_devices.append(
            HueBridgeDeviceDiscoveryInfo(
                id=info.properties[b"bridgeid"],
                ip_address=info.parsed_addresses()[0],
                port=info.port,
            )
        )

    def get_service_handler(self):
        """Returns an asynchronous handler to be called when a service state changes (To be passed to AsyncServiceBrowser)

        See https://github.com/python-zeroconf/python-zeroconf/blob/master/examples/async_browser.py
        """

        def async_on_service_state_change(
            zeroconf: Zeroconf,
            service_type: str,
            name: str,
            state_change: ServiceStateChange,
        ) -> None:
            if state_change is ServiceStateChange.Added:
                asyncio.ensure_future(self.add_service(zeroconf, service_type, name))
            else:
                return

        return async_on_service_state_change

    def get_found_devices(self) -> list[HueBridgeDeviceDiscoveryInfo]:
        """Returns all the found devices"""
        return self._found_devices


class HueBridgeDiscovery:
    """Contains methods to discover Hue Bridge devices."""

    @staticmethod
    async def discover(use_mDNS: bool) -> list[HueBridgeDeviceDiscoveryInfo]:
        """Attempts to discover all Hue Bridges that are available on the current network.

        :param use_mDNS: Whether to use mDNS discovery. This may not work in some configurations such as Docker via WSL.
        """
        if use_mDNS:
            zeroconf = AsyncZeroconf()
            listener = HueBridgeDiscoveryListener()
            browser = AsyncServiceBrowser(
                zeroconf.zeroconf,
                "_hue._tcp.local.",
                handlers=[listener.get_service_handler()],
            )
            # Wait 5 seconds to collect as many as possible
            await asyncio.sleep(5)

            await browser.async_cancel()
            await zeroconf.async_close()

            return listener.get_found_devices()
        else:
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get(DISCOVER_URL)
                    response.raise_for_status()
                    found_devices = response.json()
                except Exception as exc:
                    raise DeviceDiscoveryError(
                        f"Unable to discover Hue Bridges due to an error during discovery '{response.reason_phrase}'"
                    ) from exc
                # Rename this as different to schema model
                for device in found_devices:
                    device["ip_address"] = device["internalipaddress"]
                    del device["internalipaddress"]
                return TypeAdapter(list[HueBridgeDeviceDiscoveryInfo]).validate_python(found_devices)

    @staticmethod
    async def authenticate(
        name: str, discovery_info: HueBridgeDeviceDiscoveryInfo, settings: HueSettings
    ) -> HueBridgeDeviceInDB:
        """Attempts to discover and authenticate a Hue Bridge device given its discovery info.

        :param name: Name to give the device.
        :param discovery_info: Device discovery info.
        :param settings: Hue settings for authentication.
        :raises HueBridgeButtonNotPressedError: If the authentication fails due to a requirement to press the button on the Hue Bridge.
        :raises DeviceAuthenticationError: If the authentication fails due to any other reason.
        """

        async with create_hue_bridge_session(discovery_info, settings) as session:
            response = await session.api.generate_client_key()
            if response.error is not None:
                if response.error.type == 101:
                    raise HueBridgeButtonNotPressedError(
                        f"Please press the button on the Hue Bridge with name '{name}' and IP '{discovery_info.ip_address}'"
                    )
            elif response.success is not None:
                return HueBridgeDeviceInDB(
                    name=name,
                    ip_address=discovery_info.ip_address,
                    port=discovery_info.port,
                    identifier=discovery_info.id,
                    username=response.success.username,
                    client_key=response.success.clientkey,
                )

        raise DeviceAuthenticationError(
            f"Failed to authenticate the Hue Bridge with name '{name}' and IP '{discovery_info.ip_address}'"
        )
