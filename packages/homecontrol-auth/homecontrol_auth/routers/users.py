from fastapi import APIRouter, status

from homecontrol_auth.dependencies import AdminUser
from homecontrol_auth.schemas.users import User, UserPatch, UserPost
from homecontrol_auth.service.core import AuthServiceDep

users = APIRouter(prefix="/users", tags=["users"])


@users.post("", summary="Create a user", status_code=status.HTTP_201_CREATED)
async def create(user: UserPost, auth_service: AuthServiceDep) -> User:
    return await auth_service.users.create(user)


@users.get("", summary="Get a list of users")
async def get_all(auth_service: AuthServiceDep, _: AdminUser) -> list[User]:
    return await auth_service.users.get_all()


@users.patch("/{user_id}", summary="Update a user")
async def patch(user_id: str, user_patch: UserPatch, auth_service: AuthServiceDep, _: AdminUser) -> User:
    return await auth_service.users.update(user_id, user_patch)


@users.delete("/{user_id}", summary="Delete a user", status_code=status.HTTP_204_NO_CONTENT)
async def delete(user_id: str, auth_service: AuthServiceDep, _: AdminUser) -> None:
    await auth_service.users.delete(user_id)
