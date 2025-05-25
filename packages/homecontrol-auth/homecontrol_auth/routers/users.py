from fastapi import APIRouter, status

from homecontrol_auth.dependencies import AdminUser
from homecontrol_auth.schemas.users import User, UserPost
from homecontrol_auth.service.core import AuthServiceDep

users = APIRouter(prefix="/users", tags=["users"])


@users.post("", summary="Create a user", status_code=status.HTTP_201_CREATED)
async def create(user: UserPost, auth_service: AuthServiceDep) -> User:
    return await auth_service.users.create(user)


@users.get("", summary="Get a list of users")
async def get_all(auth_service: AuthServiceDep, _: AdminUser) -> list[User]:
    return await auth_service.users.get_all()
