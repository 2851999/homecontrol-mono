from homecontrol_base_api.types import StringUUID
from pydantic import BaseModel, ConfigDict, Field


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
