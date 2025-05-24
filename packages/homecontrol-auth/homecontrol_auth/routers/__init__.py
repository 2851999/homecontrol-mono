from fastapi import APIRouter, status
from homecontrol_auth.schemas.users import UserPost, User


users = APIRouter(prefix="/users", tags=["users"])


@users.post("", summary="Create a user", status_code=status.HTTP_201_CREATED)
async def create(user: UserPost) -> User:
    pass
