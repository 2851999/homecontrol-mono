import asyncio
from typing import Optional

from homecontrol_controller.devices.hue.api.schemas import RoomGet
from homecontrol_controller.devices.hue.api.session import HueBridgeAPISession
from homecontrol_controller.devices.hue.colour import HueColour
from homecontrol_controller.schemas.hue import (
    HueGroupedLightState,
    HueLight,
    HueLightState,
    HueRoom,
    HueRoomState,
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
