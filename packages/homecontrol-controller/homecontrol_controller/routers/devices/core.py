from fastapi import APIRouter

from homecontrol_controller.routers.devices.aircon import aircon
from homecontrol_controller.routers.devices.hue import hue

devices = APIRouter(prefix="/devices")

devices.include_router(aircon)
devices.include_router(hue)
