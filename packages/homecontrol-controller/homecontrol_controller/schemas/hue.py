from enum import StrEnum
from typing import Optional

from homecontrol_base_api.types import StringUUID
from pydantic import BaseModel, ConfigDict

from homecontrol_controller.devices.hue.colour import HueColour


class HueBridgeDeviceDiscoveryInfo(BaseModel):
    """Schema for a discovered Hue Bridge device."""

    id: str
    ip_address: str
    port: int


class HueBridgeDevicePost(BaseModel):
    """Schema for creating a Hue Bridge device."""

    name: str
    discovery_info: HueBridgeDeviceDiscoveryInfo


class HueBridgeDevice(HueBridgeDeviceDiscoveryInfo):
    """Schema for a Hue Bridge device."""

    model_config = ConfigDict(from_attributes=True)

    id: StringUUID


class HueLight(BaseModel):
    id: str
    name: str


class HueScene(BaseModel):
    id: str
    name: str


class HueRoom(BaseModel):
    """Schema for a room managed by a Hue bridge."""

    id: str
    name: str
    grouped_light_id: Optional[str]
    lights: list[HueLight]
    scenes: list[HueScene]


class HueGroupedLightState(BaseModel):
    """Schema for the state of a grouped light managed by a Hue bridge."""

    id: str
    on: bool
    brightness: float


class HueLightState(BaseModel):
    """Schema for the state of a light managed by a Hue bridge."""

    id: str
    name: str
    on: bool

    # Will be None for a Hue smart plug
    brightness: Optional[float] = None
    colour_temperature: Optional[int] = None
    colour: Optional[HueColour] = None


class HueSceneStatus(StrEnum):
    INACTIVE = "inactive"
    STATIC = "static"
    DYNAMIC_PALETTE = "dynamic_palette"


class HueSceneState(BaseModel):
    id: str
    name: str
    status: HueSceneStatus


class HueRoomState(BaseModel):
    """Schema for the state of a room managed by a Hue bridge."""

    grouped_light: HueGroupedLightState
    lights: list[HueLightState]
    scenes: list[HueSceneState]
