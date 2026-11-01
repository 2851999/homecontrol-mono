from enum import StrEnum
from typing import Annotated, Literal

from homecontrol_base_api.types import StringUUID, UUIDString
from pydantic import BaseModel, ConfigDict, Field

from homecontrol_controller.schemas.aircon import ACDeviceStatePatch


class TaskType(StrEnum):
    """Available task types."""

    # Air conditioning state
    AC_STATE = "ac_state"
    # Phillip's Hue Scene
    HUE_SCENE = "hue_scene"


class TaskACState(BaseModel):
    """Schema for an AC state task."""

    type: Literal[TaskType.AC_STATE]
    device_id: StringUUID
    state: ACDeviceStatePatch


class TaskHueScene(BaseModel):
    """Schema for a Hue Scene task."""

    type: Literal[TaskType.HUE_SCENE]
    bridge_id: StringUUID
    room_id: StringUUID
    scene_id: StringUUID


Task = Annotated[TaskACState | TaskHueScene, Field(discriminator="type")]


class RoomActionPost(BaseModel):
    """Schema for creating a room action."""

    name: str
    room_id: UUIDString
    icon: str
    tasks: list[Task]


class RoomAction(RoomActionPost):
    """Schema for a room action."""

    model_config = ConfigDict(from_attributes=True)

    id: StringUUID
    room_id: StringUUID
