from fastapi import APIRouter, status

from homecontrol_controller.routers.devices.aircon import aircon

devices = APIRouter(prefix="/devices")

devices.include_router(aircon)
