import asyncio

from homecontrol_base_api.database.core import get_database
from homecontrol_base_api.exceptions import BaseAPIError, handle_base_api_error
from msmart.discover import Discover

from homecontrol_controller.config import settings
from homecontrol_controller.database.core import ControllerDatabaseSession
from homecontrol_controller.devices.aircon.discovery import ACDiscovery
from homecontrol_controller.devices.aircon.manager import ACManager
from homecontrol_controller.devices.hue.api.schemas import GroupedLightPut, LightPut, ScenePut
from homecontrol_controller.devices.hue.manager import HueBridgeManager
from homecontrol_controller.routers.devices.core import devices


async def async_main():

    # Doesn't work on WSL
    # devices = await Discover.discover()
    # print(devices)

    # Does work on WSL
    # device = await ACManager.discover(
    #     name="Test",
    #     ip_address="192.168.1.246",
    #     settings=settings.midea,
    # )
    # print(device)

    # print(await discover_hue_bridges(False))

    # print(await ACDiscovery.discover(settings.midea))

    hue_bridge_manager = HueBridgeManager()
    async with get_database(ControllerDatabaseSession, settings.database) as database:
        async with database.start_session() as session:
            hue_bridge_devices = await session.hue_bridge_devices.get_all()
            hue_bridge_manager.add_all(hue_bridge_devices)

    device = hue_bridge_manager.get("b645c0cc-1890-4878-8df9-6f12f9cae5b4")
    async with device.connect() as session:
        # print(await session.api.get_lights())
        # print(await session.api.get_light("56c4f442-0952-4a75-ac29-7259970b3139"))
        # print(await session.api.put_light("9c76db66-26ad-43ee-b3b1-915be3060a4c", LightPut(on={"on": False})))
        # print(await session.api.get_scenes())
        # print(await session.api.get_scene("2dafd662-78cc-4594-8daf-b211434729a5"))
        # print(
        #     await session.api.put_scene("b711b49f-0bb7-4a9a-b730-2bc6ca29c450", ScenePut(recall={"action": "active"}))
        # )
        # print(await session.api.get_rooms())
        # print(await session.api.get_room("e7e6883f-85ae-4d28-8dab-7b783445acad"))
        # print(await session.api.get_grouped_lights())
        # print(await session.api.get_grouped_light("42e245c4-ef2a-447c-9b55-0f657862b0ac"))
        print(
            await session.api.put_grouped_light(
                "42e245c4-ef2a-447c-9b55-0f657862b0ac", GroupedLightPut(on={"on": False})
            )
        )


asyncio.run(async_main())
