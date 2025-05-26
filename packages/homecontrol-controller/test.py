import asyncio

from msmart.discover import Discover

from homecontrol_controller.config import settings


async def async_main():

    # Doesn't work on WSL
    # devices = await Discover.discover()
    # print(devices)

    # Does work on WSL
    device = await Discover.discover_single(
        "192.168.1.246",
        account=settings.midea_username,
        password=settings.midea_password.get_secret_value(),
    )
    print(device)


asyncio.run(async_main())
