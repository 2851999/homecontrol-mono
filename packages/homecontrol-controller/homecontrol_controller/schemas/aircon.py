from enum import IntEnum
from typing import Optional

from homecontrol_base_api.types import StringUUID
from msmart.device.AC.device import AirConditioner
from pydantic import BaseModel, ConfigDict


class ACDeviceDiscoveryInfo(BaseModel):
    "Schema for a discovered AC device."

    model_config = ConfigDict(from_attributes=True)

    id: int
    ip_address: str


class ACDevicePost(BaseModel):
    """Schema for creating an AC device."""

    name: str
    discovery_info: ACDeviceDiscoveryInfo


class ACDevice(ACDeviceDiscoveryInfo):
    """Schema for an AC device."""

    model_config = ConfigDict(from_attributes=True)

    id: StringUUID


class ACDeviceMode(IntEnum):
    """Wrapper for AC device modes."""

    AUTO = AirConditioner.OperationalMode.AUTO  # 1
    COOL = AirConditioner.OperationalMode.COOL  # 2
    DRY = AirConditioner.OperationalMode.DRY  # 3
    HEAT = AirConditioner.OperationalMode.HEAT  # 4
    FAN = AirConditioner.OperationalMode.FAN_ONLY  # 5


class ACDeviceFanSpeed(IntEnum):
    """Wrapper for AC device fan speeds."""

    AUTO = AirConditioner.FanSpeed.AUTO  # 102
    MAX = AirConditioner.FanSpeed.MAX  # 100
    HIGH = AirConditioner.FanSpeed.HIGH  # 80
    MEDIUM = AirConditioner.FanSpeed.MEDIUM  # 60
    LOW = AirConditioner.FanSpeed.LOW  # 40
    SILENT = AirConditioner.FanSpeed.SILENT  # 20


class ACDeviceSwingMode(IntEnum):
    """Wrapper for AC device swing modes."""

    OFF = AirConditioner.SwingMode.OFF  # 0x0, 0
    VERTICAL = AirConditioner.SwingMode.VERTICAL  # 0xC, 12
    HORIZONTAL = AirConditioner.SwingMode.HORIZONTAL  # 0x3, 3
    BOTH = AirConditioner.SwingMode.BOTH  # 0xF, 14


class ACDeviceRate(IntEnum):
    """Wrapper for AC device rates"""

    OFF = AirConditioner.RateSelect.OFF  # 100
    GEAR_50 = AirConditioner.RateSelect.GEAR_50  # 50
    GEAR_75 = AirConditioner.RateSelect.GEAR_75  # 75


class ACDeviceState(BaseModel):
    """Schema for an AC device's state."""

    # Read and write
    power: bool
    target_temperature: float
    operational_mode: ACDeviceMode
    fan_speed: ACDeviceFanSpeed
    swing_mode: ACDeviceSwingMode
    eco_mode: bool
    turbo_mode: bool
    rate: ACDeviceRate
    fahrenheit: bool
    display_on: bool

    # Read only
    indoor_temperature: float
    outdoor_temperature: float


class ACDeviceStatePatch(BaseModel):
    """Schema for an AC device's state patch."""

    # Read and write
    power: bool | None = None
    target_temperature: float | None = None
    operational_mode: ACDeviceMode | None = None
    fan_speed: ACDeviceFanSpeed | None = None
    swing_mode: ACDeviceSwingMode | None = None
    eco_mode: bool | None = None
    turbo_mode: bool | None = None
    rate: ACDeviceRate | None = None
    fahrenheit: bool | None = None
    display_on: bool | None = None

    # Write only
    beep: bool | None = None
