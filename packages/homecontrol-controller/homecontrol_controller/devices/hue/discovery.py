import asyncio

import httpx
from pydantic import TypeAdapter
from zeroconf import ServiceStateChange, Zeroconf
from zeroconf.asyncio import AsyncServiceBrowser, AsyncServiceInfo, AsyncZeroconf

from homecontrol_controller.exceptions import DeviceDiscoveryError
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
                internalipaddress=info.parsed_addresses()[0],
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
                response = await client.get(DISCOVER_URL)
                if response.is_error:
                    raise DeviceDiscoveryError(
                        f"Unable to discover Hue Bridges due to an error during discovery '{response.reason_phrase}'"
                    )
                return TypeAdapter(list[HueBridgeDeviceDiscoveryInfo]).validate_python(response.json())
