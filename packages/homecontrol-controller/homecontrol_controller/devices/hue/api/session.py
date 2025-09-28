from typing import Type, TypeVar

from httpx import AsyncClient
from pydantic import BaseModel, TypeAdapter

from homecontrol_controller.devices.hue.api.schemas import (
    DeviceGet,
    GroupedLightGet,
    GroupedLightPut,
    HueBridgeAPIPostResponse,
    LightGet,
    LightPut,
    ResourceIdentifierGet,
    RoomGet,
    RoomPut,
    SceneGet,
    ScenePut,
)
from homecontrol_controller.exceptions import DeviceAuthenticationError

T = TypeVar("T", bound=BaseModel)


class HueBridgeAPISession:
    """Handles communication with a Hue Bridge according to the Hue v2 API."""

    _client: AsyncClient
    _bridge_identifier: str

    def __init__(self, client: AsyncClient, bridge_identifier: str):
        """Intitialise this session for communicating with a specific Hue Bridge.

        :param client: AsyncClient from httpx.
        :param bridge_identifier: Identifier of the Hue Bridge - used for SSL verification.
        """
        self._client = client
        self._bridge_identifier = bridge_identifier

    async def generate_client_key(self) -> HueBridgeAPIPostResponse:
        """Attempts to generate a clientkey for a Hue Bridge device.

        :return: The response information.
        """

        try:
            response = await self._client.post(
                "/api",
                json={"devicetype": "homecontrol#controller", "generateclientkey": True},
                extensions={"sni_hostname": self._bridge_identifier},
            )
            response.raise_for_status()
            return HueBridgeAPIPostResponse.model_validate(response.json()[0])
        except Exception as exc:
            raise DeviceAuthenticationError("Unable to generate client key for the Hue Bridge") from exc

    async def _get_resource(self, endpoint: str, resource_type: Type[T]) -> list[T]:
        """Returns parsed data from a get request to an endpoint.

        :param endpoint: Endpoint to call.
        :param resource_type: Pydantic model type to parse the data to.
        :return: Pydantic model containing the returned data.
        """

        response = await self._client.get(endpoint)
        # TODO: Better error handling here (same for put)
        response.raise_for_status()
        return TypeAdapter(list[resource_type]).validate_python(response.json()["data"])

    async def _put_resource(self, endpoint: str, resource: T) -> ResourceIdentifierGet:
        """Put request of a resource to an endpoint.

        :param endpoint: Endpoint to call.
        :param resource_type: Pydantic model containing the data to put.
        :return: Pydantic model containing the returned data.
        """

        response = await self._client.put(endpoint, json=resource.model_dump(exclude_unset=True))
        response.raise_for_status()
        return TypeAdapter(list[ResourceIdentifierGet]).validate_python(response.json()["data"])[0]

    # --------------------------------------- Lights ---------------------------------------

    async def get_lights(self) -> list[LightGet]:
        return await self._get_resource("/clip/v2/resource/light", LightGet)

    async def get_light(self, light_id: str) -> LightGet:
        return (await self._get_resource(f"/clip/v2/resource/light/{light_id}", LightGet))[0]

    async def put_light(self, light_id: str, data: LightPut) -> ResourceIdentifierGet:
        return await self._put_resource(f"/clip/v2/resource/light/{light_id}", data)

    # --------------------------------------- Scenes ---------------------------------------

    async def get_scenes(self) -> list[SceneGet]:
        return await self._get_resource("/clip/v2/resource/scene", SceneGet)

    async def get_scene(self, scene_id: str) -> SceneGet:
        return (await self._get_resource(f"/clip/v2/resource/scene/{scene_id}", SceneGet))[0]

    async def put_scene(self, scene_id: str, data: ScenePut) -> ResourceIdentifierGet:
        return await self._put_resource(f"/clip/v2/resource/scene/{scene_id}", data)

    # --------------------------------------- Rooms ---------------------------------------

    async def get_rooms(self) -> list[RoomGet]:
        return await self._get_resource("/clip/v2/resource/room", RoomGet)

    async def get_room(self, room_id: str) -> RoomGet:
        return (await self._get_resource(f"/clip/v2/resource/room/{room_id}", RoomGet))[0]

    async def put_room(self, room_id, data: RoomPut) -> ResourceIdentifierGet:
        return await self._put_resource(f"/clip/v2/resource/room/{room_id}", data)

    # ----------------------------------- GroupedLights -----------------------------------

    async def get_grouped_lights(self) -> list[GroupedLightGet]:
        return await self._get_resource("/clip/v2/resource/grouped_light", GroupedLightGet)

    async def get_grouped_light(self, grouped_light_id: str) -> GroupedLightGet:
        return (await self._get_resource(f"/clip/v2/resource/grouped_light/{grouped_light_id}", GroupedLightGet))[0]

    async def put_grouped_light(self, grouped_light_id: str, data: GroupedLightPut) -> GroupedLightPut:
        return await self._put_resource(f"/clip/v2/resource/grouped_light/{grouped_light_id}", data)

    # --------------------------------------- Devices ---------------------------------------

    async def get_devices(self) -> list[DeviceGet]:
        return await self._get_resource("/clip/v2/resource/device", DeviceGet)

    async def get_device(self, device_id: str) -> DeviceGet:
        return (await self._get_resource(f"/clip/v2/resource/device/{device_id}", DeviceGet))[0]
