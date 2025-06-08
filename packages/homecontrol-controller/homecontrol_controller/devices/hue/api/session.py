from httpx import AsyncClient

from homecontrol_controller.devices.hue.api.schemas import HueBridgeAPIPostResponse
from homecontrol_controller.exceptions import DeviceAuthenticationError


class HueBridgeAPISession:
    """Handles communication with a Hue Bridge according to the Hue v2 API."""

    _client: AsyncClient
    _bridge_identifier: str

    def __init__(self, client: AsyncClient, bridge_identifier: str):
        """Intitialise this session for communicating with a specific Hue Bridge.

        :param client: AsyncClient form httpx.
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
