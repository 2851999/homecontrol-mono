from fastapi import APIRouter, status

from homecontrol_auth.schemas.users import UserPost, User
from homecontrol_auth.service.core import AuthServiceDep


users = APIRouter(prefix="/users", tags=["auth"])

@users.post("", summary="Create a user", status_code=status.HTTP_201_CREATED)
async def create(user: UserPost, auth_service: AuthServiceDep) -> User:
    return await auth_service.users.create(user)
