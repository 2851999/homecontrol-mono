from homecontrol_base_api.types import StringUUID
from pydantic import BaseModel


class ACDevicePost(BaseModel):
    """Schema for creating an AC device."""

    name: str
    ip_address: str


class ACDevice(ACDevicePost):
    """Schema for an AC device."""

    id: StringUUID
