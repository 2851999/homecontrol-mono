from pydantic import BaseModel


class HueBridgeDiscoveryInfo(BaseModel):
    """Schema for a discovered Hue Bridge"""

    id: str
    internalipaddress: str
    port: int
