from typing import Annotated, Literal, Optional, TypeVar

from pydantic import BaseModel, BeforeValidator

# -------------------- Post response from a Hue Bridge's /api endpoint --------------------


class HueBridgeAPIPostResponseSuccess(BaseModel):
    username: str
    clientkey: str


class HueBridgeAPIPostResponseError(BaseModel):
    type: int
    address: str
    description: str


class HueBridgeAPIPostResponse(BaseModel):

    success: Optional[HueBridgeAPIPostResponseSuccess] = None
    error: Optional[HueBridgeAPIPostResponseError] = None


# ------------------------------------- General other -------------------------------------


class ResourceIdentifierGet(BaseModel):
    rid: str
    rtype: str


# --------------------------------------- LightGet ---------------------------------------


class OwnerGet(BaseModel):
    rid: str
    rtype: str


class LightMetadataGet(BaseModel):
    name: str
    fixed_mired: Optional[int] = None
    function: str


class ProductDataGet(BaseModel):
    name: Optional[str] = None
    archetype: Optional[str] = None
    function: str


class OnGet(BaseModel):
    on: bool


class DimmingGet(BaseModel):
    brightness: float
    min_dim_level: Optional[float] = None


class MirekSchemaGet(BaseModel):
    mirek_minimum: int
    mirek_maximum: int


class ColorTemperatureGet(BaseModel):
    mirek: Optional[int]
    mirek_valid: bool
    mirek_schema: MirekSchemaGet


class XYGet(BaseModel):
    x: float
    y: float


class GamutGet(BaseModel):
    red: XYGet
    green: XYGet
    blue: XYGet


class ColorGet(BaseModel):
    xy: XYGet
    gamut: Optional[GamutGet]
    gamut_type: str


class LightDynamicsGet(BaseModel):
    status: str
    status_values: list[str]
    speed: float
    speed_valid: bool


class AlertGet(BaseModel):
    action_values: list[str]


class SignallingStatusGet(BaseModel):
    signal: str
    estimated_end: str  # TODO: Datetime
    colors: list[ColorGet]


class SignallingGet(BaseModel):
    signal_values: list[str]
    status: Optional[SignallingStatusGet] = None


class GradientPointGet(BaseModel):
    color: ColorGet


class GradientGet(BaseModel):
    points: list[GradientPointGet]
    mode: str
    points_capable: int
    mode_values: list[str]
    pixel_count: Optional[int] = None


class EffectsV2ActionGet(BaseModel):
    effect_values: list[str]


class ParametersColorGet(BaseModel):
    xy: XYGet


class ParametersColorTemperatureGet(BaseModel):
    mirek: int
    mirek_valid: bool


class ParametersGet(BaseModel):
    color: Optional[ParametersColorGet] = None
    color_temperature: Optional[ParametersColorTemperatureGet] = None
    speed: float


class EffectsV2StatusGet(BaseModel):
    effect: str
    effect_values: list[str]
    parameters: Optional[ParametersGet] = None


class EffectsV2Get(BaseModel):
    action: EffectsV2ActionGet
    status: EffectsV2StatusGet


class TimedEffectsGet(BaseModel):
    status_values: list[str]
    status: str
    effect_values: list[str]


class PowerupOnGet(BaseModel):
    mode: str
    on: Optional[OnGet] = None


class PowerupDimmingDimmingGet(BaseModel):
    brightness: float


class PowerupDimmingGet(BaseModel):
    mode: str
    dimming: Optional[PowerupDimmingDimmingGet] = None


class PowerupColorColorTemperatureGet(BaseModel):
    mirek: int


class PowerupColorGet(BaseModel):
    mode: str
    color_temperature: Optional[PowerupColorColorTemperatureGet] = None
    color: Optional[XYGet] = None


class PowerupGet(BaseModel):
    preset: str
    configured: bool
    on: PowerupOnGet
    dimming: Optional[PowerupDimmingGet] = None
    color: Optional[PowerupColorGet] = None


class LightGet(BaseModel):
    type: Literal["light"]
    id: str
    owner: OwnerGet
    metadata: LightMetadataGet
    product_data: Optional[ProductDataGet] = None
    service_id: int
    on: OnGet
    dimming: Optional[DimmingGet] = None
    color_temperature: Optional[ColorTemperatureGet] = None
    color: Optional[ColorGet] = None
    dynamics: Optional[LightDynamicsGet] = None
    alert: Optional[AlertGet] = None
    signalling: Optional[SignallingGet] = None
    mode: str
    gradient: Optional[GradientGet] = None
    effects_v2: Optional[EffectsV2Get] = None
    timed_effects: Optional[TimedEffectsGet] = None
    powerup: Optional[PowerupGet] = None


# --------------------------------------- LightPut ---------------------------------------


class LightMetadataPut(BaseModel):
    name: Optional[str] = None
    function: Optional[Literal["functional", "decorative", "mixed", "unknown"]]


class IdentifyPut(BaseModel):
    action: Literal["identify"]


class OnPut(BaseModel):
    on: Optional[bool] = None


class DimmingPut(BaseModel):
    brightness: Optional[float] = None


class DimmingDeltaPut(BaseModel):
    action: Literal["up", "down", "stop"]
    brightness_delta: Optional[int] = None


class ColorTemperaturePut(BaseModel):
    mirek: Optional[int] = None


class ColorTemperatureDeltaPut(BaseModel):
    action: Literal["up", "down", "stop"]
    mirek_delta: Optional[int] = None


class XYPut(BaseModel):
    x: float
    y: float


class ColorPut(BaseModel):
    xy: Optional[XYPut] = None


class LightDynamicsPut(BaseModel):
    duration: Optional[int] = None
    speed: Optional[float] = None


class AlertPut(BaseModel):
    action: Literal["breathe"]


class SignallingPut(BaseModel):
    signal: Literal["no_signal", "on_off", "on_off_color", "alternating"]
    duration: int
    colors: list[ColorPut]


class GradientPointPut(BaseModel):
    color: ColorPut


class GradientPut(BaseModel):
    points: list[GradientPointPut]
    mode: Optional[Literal["interpolated_palette", "interpolated_palette_mirrored", "random_pixelated"]] = None


class ParametersPut(BaseModel):
    color: Optional[ColorPut] = None
    color_temperature: Optional[ColorTemperaturePut] = None
    speed: Optional[float] = None


class EffectsV2ActionPut(BaseModel):
    effect: Literal[
        "prism",
        "opal",
        "glisten",
        "sparkle",
        "fire",
        "candle",
        "underwater",
        "cosmos",
        "sunbeam",
        "enchant",
        "no_effect",
    ]
    parameters: Optional[ParametersPut] = None


class EffectsV2Put(BaseModel):
    action: Optional[EffectsV2ActionPut] = None


class TimedEffectsPut(BaseModel):
    effect: Optional[Literal["sunrise", "sunset", "no_effect"]] = None
    duration: Optional[int] = None


class PowerupOnPut(BaseModel):
    mode: Literal["on", "toggle", "previous"]
    on: Optional[OnPut] = None


class PowerupDimmingPut(BaseModel):
    mode: Literal["dimming", "previous"]
    dimming: Optional[DimmingPut] = None


class PowerupColorPut(BaseModel):
    mode: Literal["color_temperature", "color", "previous"]
    color_temperature: Optional[ColorTemperaturePut] = None
    color: Optional[ColorPut] = None


class PowerupPut(BaseModel):
    preset: Literal["safety", "powerfail", "last_on_state", "custom"]
    on: Optional[PowerupOnPut] = None
    dimming: Optional[PowerupDimmingPut] = None
    color: Optional[PowerupColorPut] = None


class LightPut(BaseModel):
    type: Optional[Literal["light"]] = None
    metadata: Optional[LightMetadataPut] = None
    identify: Optional[IdentifyPut] = None
    on: Optional[OnPut] = None
    dimming: Optional[DimmingPut] = None
    dimming_delta: Optional[DimmingDeltaPut] = None
    color_temperature: Optional[ColorTemperaturePut] = None
    color_temperature_delta: Optional[ColorTemperatureDeltaPut] = None
    color: Optional[ColorPut] = None
    dynamics: Optional[LightDynamicsPut] = None
    alert: Optional[AlertPut] = None
    signalling: Optional[SignallingPut] = None
    gradient: Optional[GradientPut] = None
    effects_v2: Optional[EffectsV2Put] = None
    timed_effects: Optional[TimedEffectsPut] = None
    powerup: Optional[PowerupPut] = None


# --------------------------------------- SceneGet ---------------------------------------


class TargetGet(BaseModel):
    rid: str
    rtype: str


class ActionDimmingGet(BaseModel):
    brightness: float


class ActionColorGet(BaseModel):
    xy: XYGet


class ActionColorTemperatureGet(BaseModel):
    mirek: int


class ActionGradientGet(BaseModel):
    points: list[GradientPointGet]
    mode: str


class ActionParametersGet(BaseModel):
    color: Optional[ParametersColorGet] = None
    color_temperature: Optional[ParametersColorTemperatureGet] = None
    speed: Optional[float] = None


class ActionEffectsV2ActionGet(BaseModel):
    effect: str
    parameters: Optional[ActionParametersGet] = None


class EffectsV2BasicGet(BaseModel):
    action: ActionEffectsV2ActionGet


class ActionDynamicsGet(BaseModel):
    duration: Optional[int] = None


class ActionActionGet(BaseModel):
    on: Optional[OnGet] = None
    dimming: Optional[ActionDimmingGet] = None
    color: Optional[ActionColorGet] = None
    color_temperature: Optional[ActionColorTemperatureGet] = None
    gradient: Optional[ActionGradientGet] = None
    effects_v2: Optional[EffectsV2BasicGet] = None
    dynamics: Optional[ActionDynamicsGet] = None


class ActionGet(BaseModel):
    target: TargetGet
    action: ActionActionGet


class PaletteColorColorGet(BaseModel):
    xy: XYGet


class PaletteDimmingGet(BaseModel):
    brightness: float


class PaletteColorGet(BaseModel):
    color: PaletteColorColorGet
    dimming: PaletteDimmingGet


class ColorTemperatureColorTemperatureGet(BaseModel):
    mirek: int


class PaletteColorTemperatureGet(BaseModel):
    color_temperature: ColorTemperatureColorTemperatureGet
    dimming: PaletteDimmingGet


class PaletteGet(BaseModel):
    color: list[PaletteColorGet]
    dimming: list[PaletteDimmingGet]
    color_temperature: list[PaletteColorTemperatureGet]


class ImageGet(BaseModel):
    rid: str
    rtype: str


class SceneMetadataGet(BaseModel):
    name: str
    image: Optional[ImageGet] = None
    appdata: Optional[str] = None


class GroupGet(BaseModel):
    rid: str
    rtype: str


class StatusGet(BaseModel):
    active: Optional[str] = None
    last_recall: Optional[str] = None  # TODO: Datetime


class SceneGet(BaseModel):
    type: Literal["scene"]
    id: str
    actions: list[ActionGet]
    palette: Optional[PaletteGet] = None
    effects_v2: list[EffectsV2BasicGet] = []
    recall: dict  # TODO: Unsure
    metadata: SceneMetadataGet
    group: GroupGet
    speed: float
    auto_dynamic: bool
    status: StatusGet


# --------------------------------------- ScenePut ---------------------------------------


class TargetPut(BaseModel):
    rid: str
    rtype: str


class SceneActionActionDynamicsPut(BaseModel):
    duration: Optional[int] = None


class ActionActionPut(BaseModel):
    on: Optional[OnPut] = None
    dimming: Optional[DimmingPut] = None
    color: Optional[ColorPut] = None
    color_temperature: Optional[ColorTemperaturePut] = None
    gradient: Optional[GradientPut] = None
    effects_v2: Optional[EffectsV2Put] = None
    dynamics: Optional[SceneActionActionDynamicsPut] = None


class ActionPut(BaseModel):
    target: TargetPut
    action: ActionActionPut


class ColorPalettePut(BaseModel):
    color: ColorPut
    dimming: DimmingPut


class ColorTemperaturePalettePut(BaseModel):
    color_temperature: ColorTemperaturePut
    dimming: DimmingPut


class PalettePut(BaseModel):
    color: list[ColorPalettePut]
    dimming: DimmingPut
    color_temperature: list[ColorTemperaturePalettePut]
    effects_v2: list[EffectsV2Put]


class RecallPut(BaseModel):
    action: Optional[Literal["active", "dynamic", "static"]] = None
    duration: Optional[int] = None
    dimming: Optional[DimmingPut] = None


class SceneMetadataPut(BaseModel):
    name: Optional[str] = None
    appdata: Optional[str] = None


class ScenePut(BaseModel):
    type: Optional[Literal["scene"]] = None
    actions: Optional[list[ActionPut]] = None
    palette: Optional[PalettePut] = None
    recall: Optional[RecallPut] = None
    metadata: Optional[LightMetadataPut] = None
    speed: Optional[float] = None
    auto_dynamic: Optional[bool] = None


# --------------------------------------- RoomGet ---------------------------------------


class RoomMetadataGet(BaseModel):
    name: str
    archetype: str


class RoomGet(BaseModel):
    type: Literal["room"]
    id: str
    children: list[ResourceIdentifierGet]
    services: list[ResourceIdentifierGet]
    metadata: RoomMetadataGet


# --------------------------------------- RoomPut ---------------------------------------


class ResourceIdentifierPut(BaseModel):
    rid: str
    rtype: str


class RoomMetadataPut(BaseModel):
    name: Optional[str] = None
    archetype: Optional[str] = None


class RoomPut(BaseModel):
    type: Optional[Literal["room"]] = None
    children: Optional[list[ResourceIdentifierPut]] = None
    metadata: Optional[RoomMetadataPut]


# ----------------------------------- GroupedLightGet -----------------------------------


# Hue seems to give various entities as {} in grouped lights, this type auto converts them to None for consistency with
# the others
T = TypeVar("T")
LeniantOptional = Annotated[Optional[T], BeforeValidator(lambda x: x or None)]


class GroupedLightDimmingGet(BaseModel):
    brightness: float


class DimmingDeltaGet(BaseModel):
    action: Literal["up", "down", "stop"] = None
    brightness_delta: int = None


class ColorTemperatureDeltaGet(BaseModel):
    action: Literal["up", "down", "stop"]
    mirek_delta: int = None


class GroupedLightSignalingGet(BaseModel):
    signal_values: list[str]


class GroupedLightDynamicsGet(BaseModel):
    duration: int


class GroupedLightGet(BaseModel):
    type: Literal["grouped_light"]
    id: str
    owner: OwnerGet
    on: Optional[OnGet] = None
    dimming: Optional[GroupedLightDimmingGet] = None
    dimming_delta: LeniantOptional[DimmingDeltaGet] = None
    color_temperature: LeniantOptional[ColorTemperatureGet] = None
    color_temperature_delta: LeniantOptional[ColorTemperatureDeltaGet] = None
    color: LeniantOptional[ColorGet] = None
    alert: Optional[AlertGet] = None
    signalling: Optional[GroupedLightSignalingGet] = None
    dyanmics: LeniantOptional[GroupedLightDynamicsGet] = None


# ----------------------------------- GroupedLightPut -----------------------------------


class GroupedLightDynamicsPut(BaseModel):
    duration: Optional[int] = None


class GroupedLightPut(BaseModel):
    type: Optional[Literal["grouped_light"]] = None
    on: Optional[OnPut] = None
    dimming: Optional[DimmingPut] = None
    dimming_delta: Optional[DimmingDeltaPut] = None
    color_temperature: Optional[ColorTemperaturePut] = None
    color_temperature_delta: Optional[ColorTemperatureDeltaPut] = None
    color: Optional[ColorPut] = None
    alert: Optional[AlertPut] = None
    signaling: Optional[SignallingPut] = None
    dyanmics: Optional[GroupedLightDynamicsPut] = None
