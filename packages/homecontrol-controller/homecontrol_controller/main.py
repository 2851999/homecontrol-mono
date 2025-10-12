from contextlib import asynccontextmanager

from fastapi import FastAPI
from homecontrol_base_api.database.core import get_database
from homecontrol_base_api.exceptions import BaseAPIError, handle_base_api_error

from homecontrol_controller.config import settings
from homecontrol_controller.database.core import ControllerDatabaseSession
from homecontrol_controller.devices.aircon.manager import ACManager
from homecontrol_controller.devices.hue.manager import HueBridgeManager
from homecontrol_controller.routers.devices.core import devices
from homecontrol_controller.routers.rooms import rooms


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Used to perform startup actions."""

    # Initialise all devices on startup
    ac_manager = ACManager()
    hue_bridge_manager = HueBridgeManager()
    async with get_database(ControllerDatabaseSession, settings.database) as database:
        async with database.start_session() as session:
            ac_devices = await session.ac_devices.get_all()
            await ac_manager.add_all(ac_devices)

            hue_bridge_devices = await session.hue_bridge_devices.get_all()
            hue_bridge_manager.add_all(hue_bridge_devices)

    app.state.ac_manager = ac_manager
    app.state.hue_bridge_manager = hue_bridge_manager

    yield


app = FastAPI(lifespan=lifespan)

app.add_exception_handler(BaseAPIError, handle_base_api_error)

app.include_router(devices)
app.include_router(rooms)
