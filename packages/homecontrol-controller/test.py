import asyncio

from msmart.discover import Discover

from homecontrol_controller.config import settings
from homecontrol_controller.devices.aircon.manager import ACManager


async def async_main():

    # Doesn't work on WSL
    # devices = await Discover.discover()
    # print(devices)

    # Does work on WSL
    device = await ACManager.discover(
        name="Test",
        ip_address="192.168.1.246",
        settings=settings.midea,
    )
    print(device)


asyncio.run(async_main())
