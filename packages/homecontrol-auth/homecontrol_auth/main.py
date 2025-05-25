from fastapi import FastAPI, Response
from homecontrol_auth.routers.users import users
from homecontrol_base_api.exceptions import BaseAPIError, handle_base_api_error

from homecontrol_auth.schemas.user_sessions import LoginPost, UserSession
from homecontrol_auth.service.core import AuthServiceDep

app = FastAPI()

app.include_router(users)

app.add_exception_handler(BaseAPIError, handle_base_api_error)


@app.post("/login", summary="Login as a user")
async def login(login: LoginPost, response: Response, auth_service: AuthServiceDep) -> UserSession:
    return await auth_service.user_sessions.create_session(login, response)
