from pydantic import BaseModel, Field


class HueBridgeDeviceDiscoveryInfo(BaseModel):
    """Schema for a discovered Hue Bridge device."""

    id: str
    ip_address: str = Field(validation_alias="internalipaddress")
    port: int
