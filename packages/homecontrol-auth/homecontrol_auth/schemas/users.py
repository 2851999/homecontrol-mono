from enum import StrEnum

from pydantic import BaseModel, ConfigDict
from homecontrol_base_api.types import StringUUID


class UserAccountType(StrEnum):
    DEFAULT = "default"
    ADMIN = "admin"


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: StringUUID
    username: str
    account_type: UserAccountType
    enabled: bool


class UserPost(BaseModel):
    username: str
    password: str
