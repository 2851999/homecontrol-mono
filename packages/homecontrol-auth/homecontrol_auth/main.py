from fastapi import FastAPI, Response, status
from homecontrol_base_api.exceptions import BaseAPIError, handle_base_api_error

from homecontrol_auth.dependencies import AnySession, AnyUser, RefreshToken
from homecontrol_auth.routers.users import users
from homecontrol_auth.schemas.user_sessions import LoginPost, UserSession
from homecontrol_auth.schemas.users import User
from homecontrol_auth.service.core import AuthServiceDep

app = FastAPI()

app.include_router(users)

app.add_exception_handler(BaseAPIError, handle_base_api_error)


@app.post("/login", summary="Login as a user")
async def login(login: LoginPost, response: Response, auth_service: AuthServiceDep) -> UserSession:
    return await auth_service.user_sessions.create(login, response)


@app.get("/verify", summary="Check authentication")
async def verify(user: AnyUser) -> User:
    return user


@app.post("/refresh", summary="Refresh user session")
async def refresh(refresh_token: RefreshToken, response: Response, auth_service: AuthServiceDep) -> UserSession:
    return await auth_service.user_sessions.refresh(refresh_token, response)


@app.post("/logout", summary="Logout as a user", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response, auth_service: AuthServiceDep, user_session: AnySession) -> None:
    await auth_service.user_sessions.delete(user_session.id, response)
