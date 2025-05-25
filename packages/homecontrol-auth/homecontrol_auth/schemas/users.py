from enum import StrEnum

from pydantic import BaseModel, ConfigDict, SecretStr
from homecontrol_base_api.types import StringUUID


class UserAccountType(StrEnum):
    """Account types"""

    DEFAULT = "default"
    ADMIN = "admin"


class User(BaseModel):
    """Schema for a user"""

    model_config = ConfigDict(from_attributes=True)

    id: StringUUID
    username: str
    account_type: UserAccountType
    enabled: bool


class UserPost(BaseModel):
    """Schema for creating a user"""

    username: str
    password: SecretStr