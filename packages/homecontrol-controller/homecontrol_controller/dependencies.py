from typing import Annotated, AsyncGenerator

from fastapi import Depends, Request

from homecontrol_controller.services.core import ControllerService, create_controller_service


async def get_controller_service(request: Request) -> AsyncGenerator[ControllerService, None]:
    """Creates an instance of the auth service"""

    async with create_controller_service(request.app.state.ac_manager) as service:
        yield service


ControllerServiceDep = Annotated[ControllerService, Depends(get_controller_service)]
