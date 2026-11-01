from typing import Annotated, Literal, TypeVar

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
    success: HueBridgeAPIPostResponseSuccess | None = None
    error: HueBridgeAPIPostResponseError | None = None


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
    fixed_mired: int | None = None
    function: str


class LightProductDataGet(BaseModel):
    name: str | None = None
    archetype: str | None = None
    function: str


class OnGet(BaseModel):
    on: bool


class DimmingGet(BaseModel):
    brightness: float
    min_dim_level: float | None = None


class MirekSchemaGet(BaseModel):
    mirek_minimum: int
    mirek_maximum: int


class ColorTemperatureGet(BaseModel):
    mirek: int | None
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
    gamut: GamutGet | None
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
    status: SignallingStatusGet | None = None


class GradientPointGet(BaseModel):
    color: ColorGet


class GradientGet(BaseModel):
    points: list[GradientPointGet]
    mode: str
    points_capable: int
    mode_values: list[str]
    pixel_count: int | None = None


class EffectsV2ActionGet(BaseModel):
    effect_values: list[str]


class ParametersColorGet(BaseModel):
    xy: XYGet


class ParametersColorTemperatureGet(BaseModel):
    mirek: int
    mirek_valid: bool


class ParametersGet(BaseModel):
    color: ParametersColorGet | None = None
    color_temperature: ParametersColorTemperatureGet | None = None
    speed: float


class EffectsV2StatusGet(BaseModel):
    effect: str
    effect_values: list[str]
    parameters: ParametersGet | None = None


class EffectsV2Get(BaseModel):
    action: EffectsV2ActionGet
    status: EffectsV2StatusGet


class TimedEffectsGet(BaseModel):
    status_values: list[str]
    status: str
    effect_values: list[str]


class PowerupOnGet(BaseModel):
    mode: str
    on: OnGet | None = None


class PowerupDimmingDimmingGet(BaseModel):
    brightness: float


class PowerupDimmingGet(BaseModel):
    mode: str
    dimming: PowerupDimmingDimmingGet | None = None


class PowerupColorColorTemperatureGet(BaseModel):
    mirek: int


class PowerupColorGet(BaseModel):
    mode: str
    color_temperature: PowerupColorColorTemperatureGet | None = None
    color: XYGet | None = None


class PowerupGet(BaseModel):
    preset: str
    configured: bool
    on: PowerupOnGet
    dimming: PowerupDimmingGet | None = None
    color: PowerupColorGet | None = None


class LightGet(BaseModel):
    type: Literal["light"]
    id: str
    owner: OwnerGet
    metadata: LightMetadataGet
    product_data: LightProductDataGet | None = None
    service_id: int
    on: OnGet
    dimming: DimmingGet | None = None
    color_temperature: ColorTemperatureGet | None = None
    color: ColorGet | None = None
    dynamics: LightDynamicsGet | None = None
    alert: AlertGet | None = None
    signalling: SignallingGet | None = None
    mode: str
    gradient: GradientGet | None = None
    effects_v2: EffectsV2Get | None = None
    timed_effects: TimedEffectsGet | None = None
    powerup: PowerupGet | None = None


# --------------------------------------- LightPut ---------------------------------------


class LightMetadataPut(BaseModel):
    name: str | None = None
    function: Literal["functional", "decorative", "mixed", "unknown"] | None


class IdentifyPut(BaseModel):
    action: Literal["identify"]


class OnPut(BaseModel):
    on: bool | None = None


class DimmingPut(BaseModel):
    brightness: float | None = None


class DimmingDeltaPut(BaseModel):
    action: Literal["up", "down", "stop"]
    brightness_delta: int | None = None


class ColorTemperaturePut(BaseModel):
    mirek: int | None = None


class ColorTemperatureDeltaPut(BaseModel):
    action: Literal["up", "down", "stop"]
    mirek_delta: int | None = None


class XYPut(BaseModel):
    x: float
    y: float


class ColorPut(BaseModel):
    xy: XYPut | None = None


class LightDynamicsPut(BaseModel):
    duration: int | None = None
    speed: float | None = None


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
    mode: Literal["interpolated_palette", "interpolated_palette_mirrored", "random_pixelated"] | None = None


class ParametersPut(BaseModel):
    color: ColorPut | None = None
    color_temperature: ColorTemperaturePut | None = None
    speed: float | None = None


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
    parameters: ParametersPut | None = None


class EffectsV2Put(BaseModel):
    action: EffectsV2ActionPut | None = None


class TimedEffectsPut(BaseModel):
    effect: Literal["sunrise", "sunset", "no_effect"] | None = None
    duration: int | None = None


class PowerupOnPut(BaseModel):
    mode: Literal["on", "toggle", "previous"]
    on: OnPut | None = None


class PowerupDimmingPut(BaseModel):
    mode: Literal["dimming", "previous"]
    dimming: DimmingPut | None = None


class PowerupColorPut(BaseModel):
    mode: Literal["color_temperature", "color", "previous"]
    color_temperature: ColorTemperaturePut | None = None
    color: ColorPut | None = None


class PowerupPut(BaseModel):
    preset: Literal["safety", "powerfail", "last_on_state", "custom"]
    on: PowerupOnPut | None = None
    dimming: PowerupDimmingPut | None = None
    color: PowerupColorPut | None = None


class LightPut(BaseModel):
    type: Literal["light"] | None = None
    metadata: LightMetadataPut | None = None
    identify: IdentifyPut | None = None
    on: OnPut | None = None
    dimming: DimmingPut | None = None
    dimming_delta: DimmingDeltaPut | None = None
    color_temperature: ColorTemperaturePut | None = None
    color_temperature_delta: ColorTemperatureDeltaPut | None = None
    color: ColorPut | None = None
    dynamics: LightDynamicsPut | None = None
    alert: AlertPut | None = None
    signalling: SignallingPut | None = None
    gradient: GradientPut | None = None
    effects_v2: EffectsV2Put | None = None
    timed_effects: TimedEffectsPut | None = None
    powerup: PowerupPut | None = None


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
    color: ParametersColorGet | None = None
    color_temperature: ParametersColorTemperatureGet | None = None
    speed: float | None = None


class ActionEffectsV2ActionGet(BaseModel):
    effect: str
    parameters: ActionParametersGet | None = None


class EffectsV2BasicGet(BaseModel):
    action: ActionEffectsV2ActionGet


class ActionDynamicsGet(BaseModel):
    duration: int | None = None


class ActionActionGet(BaseModel):
    on: OnGet | None = None
    dimming: ActionDimmingGet | None = None
    color: ActionColorGet | None = None
    color_temperature: ActionColorTemperatureGet | None = None
    gradient: ActionGradientGet | None = None
    effects_v2: EffectsV2BasicGet | None = None
    dynamics: ActionDynamicsGet | None = None


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
    image: ImageGet | None = None
    appdata: str | None = None


class GroupGet(BaseModel):
    rid: str
    rtype: str


class StatusGet(BaseModel):
    active: str | None = None
    last_recall: str | None = None  # TODO: Datetime


class SceneGet(BaseModel):
    type: Literal["scene"]
    id: str
    actions: list[ActionGet]
    palette: PaletteGet | None = None
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
    duration: int | None = None


class ActionActionPut(BaseModel):
    on: OnPut | None = None
    dimming: DimmingPut | None = None
    color: ColorPut | None = None
    color_temperature: ColorTemperaturePut | None = None
    gradient: GradientPut | None = None
    effects_v2: EffectsV2Put | None = None
    dynamics: SceneActionActionDynamicsPut | None = None


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
    action: Literal["active", "dynamic", "static"] | None = None
    duration: int | None = None
    dimming: DimmingPut | None = None


class SceneMetadataPut(BaseModel):
    name: str | None = None
    appdata: str | None = None


class ScenePut(BaseModel):
    type: Literal["scene"] | None = None
    actions: list[ActionPut] | None = None
    palette: PalettePut | None = None
    recall: RecallPut | None = None
    metadata: LightMetadataPut | None = None
    speed: float | None = None
    auto_dynamic: bool | None = None


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
    name: str | None = None
    archetype: str | None = None


class RoomPut(BaseModel):
    type: Literal["room"] | None = None
    children: list[ResourceIdentifierPut] | None = None
    metadata: RoomMetadataPut | None


# ----------------------------------- GroupedLightGet -----------------------------------


# Hue seems to give various entities as {} in grouped lights, this type auto converts them to None for consistency with
# the others
T = TypeVar("T")
LeniantOptional = Annotated[T | None, BeforeValidator(lambda x: x or None)]


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
    on: OnGet | None = None
    dimming: GroupedLightDimmingGet | None = None
    dimming_delta: LeniantOptional[DimmingDeltaGet] = None
    color_temperature: LeniantOptional[ColorTemperatureGet] = None
    color_temperature_delta: LeniantOptional[ColorTemperatureDeltaGet] = None
    color: LeniantOptional[ColorGet] = None
    alert: AlertGet | None = None
    signalling: GroupedLightSignalingGet | None = None
    dyanmics: LeniantOptional[GroupedLightDynamicsGet] = None


# ----------------------------------- GroupedLightPut -----------------------------------


class GroupedLightDynamicsPut(BaseModel):
    duration: int | None = None


class GroupedLightPut(BaseModel):
    type: Literal["grouped_light"] | None = None
    on: OnPut | None = None
    dimming: DimmingPut | None = None
    dimming_delta: DimmingDeltaPut | None = None
    color_temperature: ColorTemperaturePut | None = None
    color_temperature_delta: ColorTemperatureDeltaPut | None = None
    color: ColorPut | None = None
    alert: AlertPut | None = None
    signaling: SignallingPut | None = None
    dyanmics: GroupedLightDynamicsPut | None = None


# -------------------------------------- DeviceGet --------------------------------------


class DeviceProductDataGet(BaseModel):
    model_id: str
    manufacturer_name: str
    product_name: str
    product_archetype: str
    certified: bool
    software_version: str
    hardware_platform_type: str | None = None


class DeviceMetadataGet(BaseModel):
    name: str
    archetype: str


class UserTestGet(BaseModel):
    status: str
    usertest: bool


class DeviceModeGet(BaseModel):
    status: str
    mode: str
    mode_values: list[dict]


class DeviceGet(BaseModel):
    type: Literal["device"]
    id: str
    product_data: DeviceProductDataGet
    metadata: DeviceMetadataGet
    identify: dict | None = None
    usertest: UserTestGet | None = None
    device_mode: DeviceModeGet | None = None
    services: list[ResourceIdentifierGet]
