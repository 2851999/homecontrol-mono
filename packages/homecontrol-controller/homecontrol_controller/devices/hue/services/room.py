import asyncio
from numbers import Real
from typing import Optional

from homecontrol_controller.devices.hue.api.schemas import (
    ColorPut,
    ColorTemperaturePut,
    DimmingPut,
    GroupedLightPut,
    LightPut,
    OnPut,
    RecallPut,
    RoomGet,
    ScenePut,
)
from homecontrol_controller.devices.hue.api.session import HueBridgeAPISession
from homecontrol_controller.devices.hue.colour import HueColour
from homecontrol_controller.schemas.hue import (
    HueGroupedLightState,
    HueLight,
    HueLightState,
    HueLightStatePatch,
    HueRoom,
    HueRoomState,
    HueRoomStatePatch,
    HueScene,
    HueSceneState,
)


class HueRoomService:
    """Service that handles rooms in Hue."""

    _session: HueBridgeAPISession

    def __init__(self, session: HueBridgeAPISession):
        """Intiialise this service for controlling a room's Hue devices.

        :param session: API session for the Hue bridge.
        """
        self._session = session

    async def _get(self, room: RoomGet) -> HueRoom:
        """Constructs a HueRoom by performing the required gets to a Hue Bridge."""

        # Attempt to find a grouped light service
        grouped_light_id: Optional[str] = None
        for service in room.services:
            if service.rtype == "grouped_light":
                grouped_light_id = service.rid

        # Locate all lights
        lights: list[HueLight] = []
        for child in room.children:
            if child.rtype == "device":
                device = await self._session.get_device(child.rid)
                for service in device.services:
                    if service.rtype == "light":
                        lights.append(HueLight(id=service.rid, name=device.metadata.name))
                        break

        # Locate all scenes
        scenes: list[HueScene] = []
        hue_scenes = await self._session.get_scenes()
        for hue_scene in hue_scenes:
            if hue_scene.group.rid == room.id:
                scenes.append(HueScene(id=hue_scene.id, name=hue_scene.metadata.name))

        return HueRoom(
            id=room.id, name=room.metadata.name, grouped_light_id=grouped_light_id, lights=lights, scenes=scenes
        )

    async def get_all(self) -> list[HueRoom]:
        """Returns a list of all rooms managed by the Hue Bridge.

        :returns: List of all rooms.
        """

        rooms = await self._session.get_rooms()
        return await asyncio.gather(*(self._get(room) for room in rooms))

    async def get(self, room_id: str) -> HueRoom:
        """Obtains a room managed by the Hue Bridge given its ID.

        :param room_id: ID of the room to obtain.
        :retrurn: The obtained room.
        """

        return await self._get(await self._session.get_room(room_id))

    async def _get_light_state(self, light: HueLight) -> HueLightState:
        """Obtains the state of a light managed by the Hue Bridge given its light instance.

        :param light: Light object to obtain the state of.
        :return: The light's state.
        """

        light_state = await self._session.get_light(light.id)
        return HueLightState(
            id=light.id,
            name=light.name,
            on=light_state.on.on,
            brigntness=light_state.dimming.brightness if light_state.dimming else None,
            colour_temperature=light_state.color_temperature.mirek if light_state.color_temperature else None,
            colour=HueColour.from_xy(light_state.color.xy) if light_state.color is not None else None,
        )

    async def get_state(self, room_id: str) -> HueRoomState:
        """Obtains the state of a room managed by the Hue Bridge given its ID.

        :param room_id: ID of the room to obtain the state of.
        :return: The obtained room state.
        """

        # Obtain the room
        room = await self.get(room_id)

        # Obtain the grouped light state
        grouped_light_state = await self._session.get_grouped_light(room.grouped_light_id)

        # Obtain the states of each light
        light_states: list[HueLightState] = await asyncio.gather(
            *(self._get_light_state(light) for light in room.lights)
        )

        # Obtain the states of each scene
        scene_states: list[HueSceneState] = []
        hue_scenes = await self._session.get_scenes()
        for hue_scene in hue_scenes:
            if hue_scene.group.rid == room.id:
                scene_states.append(
                    HueSceneState(id=hue_scene.id, name=hue_scene.metadata.name, status=hue_scene.status.active)
                )

        return HueRoomState(
            grouped_light=HueGroupedLightState(
                id=grouped_light_state.id,
                on=grouped_light_state.on.on if grouped_light_state.on is not None else None,
                brightness=grouped_light_state.dimming.brightness if grouped_light_state.dimming is not None else None,
            ),
            lights=light_states,
            scenes=scene_states,
        )

    async def _update_light_state(self, light_id: str, state_patch: HueLightStatePatch):
        """Updates the state of a light in a room managed by the Hue Bridge given its ID.

        :param light_id: ID of the light to change the state of.
        :param state_patch: Change of state to apply to the light.
        """

        await self._session.put_light(
            light_id=light_id,
            data=LightPut(
                on=OnPut(on=state_patch.on) if state_patch.on is not None else None,
                dimming=DimmingPut(brightness=state_patch.brightness) if state_patch.brightness is not None else None,
                color_temperature=(
                    ColorTemperaturePut(mirek=state_patch.colour_temperature)
                    if state_patch.colour_temperature is not None
                    else None
                ),
                color=ColorPut(xy=state_patch.colour.to_xy()) if state_patch.colour is not None else None,
            ),
        )

    async def update_state(self, room_id: str, state_patch: HueRoomStatePatch) -> HueRoomState:
        """Updates the state of a room managed by the Hue Bridge given its ID.

        :param room_id: ID of the room to change the state of.
        :param state_patch: Change of state to apply to the room.
        :return: The new state of the room.
        """

        # Obtain the room itself
        room = await self.get(room_id)

        # Update the grouped light state
        if state_patch.grouped_light:
            await self._session.put_grouped_light(
                room.grouped_light_id,
                GroupedLightPut(
                    on=OnPut(on=state_patch.grouped_light.on) if state_patch.grouped_light.on is not None else None,
                    dimming=(
                        DimmingPut(brightness=state_patch.grouped_light.brightness)
                        if state_patch.grouped_light.brightness is not None
                        else None
                    ),
                ),
            )
        # Update the light states
        if state_patch.lights:
            await asyncio.gather(
                *(
                    self._update_light_state(light_id, light_state_patch)
                    for light_id, light_state_patch in state_patch.lights.items()
                )
            )
        # Recall a scene if requested (Always use active here to start any effects automatically)
        if state_patch.scene_id:
            await self._session.put_scene(state_patch.scene_id, ScenePut(recall=RecallPut(action="active")))

        # Return the new state of the room
        return await self.get_state(room_id)
