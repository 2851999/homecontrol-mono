import ssl
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator, Optional

from httpx import AsyncClient

from homecontrol_controller.database.models import HueBridgeDeviceInDB
from homecontrol_controller.devices.hue.api.session import HueBridgeAPISession
from homecontrol_controller.devices.hue.services.room import HueRoomService
from homecontrol_controller.schemas.hue import HueBridgeDeviceDiscoveryInfo


class HueBridgeSession:
    """Handles a session for contacting a Hue Bridge."""

    _client: AsyncClient
    _bridge_identifier: str
    _api: Optional[HueBridgeAPISession] = None
    _rooms: Optional[HueRoomService] = None

    def __init__(self, client: AsyncClient, bridge_identifier: str):
        """Intitialise this session for communicating with a specific Hue Bridge.

        :param client: AsyncClient from httpx.
        :param bridge_identifier: Identifier of the Hue Bridge - used for SSL verification.
        """

        self._client = client
        self._bridge_identifier = bridge_identifier

    @property
    def api(self) -> HueBridgeAPISession:
        if not self._api:
            self._api = HueBridgeAPISession(self._client, self._bridge_identifier)
        return self._api

    @property
    def rooms(self) -> HueRoomService:
        if not self._rooms:
            self._rooms = HueRoomService(self.api)
        return self._rooms


@asynccontextmanager
async def create_hue_bridge_session(
    connection_info: HueBridgeDeviceDiscoveryInfo | HueBridgeDeviceInDB,
) -> AsyncGenerator[HueBridgeSession, None]:
    """Creates a session for communicating with a specific Hue Bridge.

    :param connection_info: Schema/Model containing the required information about the Bridge. If it is an instance of
                            HueBridgeDeviceDiscoveryInfo then will assume it has not been authenticated yet. If it is
                            a HueBridgeDeviceInDB then will assume have already authenticated and should use the
                            provided credentials.
    """
    ssl_ctx = ssl.create_default_context(cafile=Path("hue_cert.pem"))
    # TODO: Explore if another way to get this to work - cant see current way to add custom hostname resolver, so just
    # disable check for now
    ssl_ctx.check_hostname = False
    authenticated = isinstance(connection_info, HueBridgeDeviceInDB)
    async with AsyncClient(
        base_url=f"https://{connection_info.ip_address}:{connection_info.port}",
        verify=ssl_ctx,
        headers=(
            {"hue-application-key": connection_info.username, "Host": f"{connection_info.identifier}.local"}
            if authenticated
            else None
        ),
    ) as client:
        yield HueBridgeSession(
            client,
            connection_info.identifier if authenticated else connection_info.id,
        )
