from enum import StrEnum
from typing import Annotated, Literal

from homecontrol_base_api.types import StringUUID
from pydantic import BaseModel, ConfigDict, Field


class ControllerType(StrEnum):
    """Available controller types."""

    # Air conditioning
    AC_DEVICE = "ac_device"
    # Phillip's Hue Room
    HUE_ROOM = "hue_room"


class ControllerACDevice(BaseModel):
    """Schema for a room controller for an air conditioning device."""

    type: Literal[ControllerType.AC_DEVICE]
    device_id: StringUUID


class ControllerHueRoom(BaseModel):
    """Schema for a room controller for a Phillp's Hue Room."""

    type: Literal[ControllerType.HUE_ROOM]
    bridge_id: StringUUID
    room_id: StringUUID


RoomController = Annotated[ControllerACDevice | ControllerHueRoom, Field(discriminator="type")]


class RoomPost(BaseModel):
    """Schema for creating a Room."""

    name: str
    controllers: list[RoomController]


class Room(RoomPost):
    """Schema for a Room."""

    model_config = ConfigDict(from_attributes=True)

    id: StringUUID
