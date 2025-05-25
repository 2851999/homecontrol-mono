from datetime import datetime
from pydantic import BaseModel, ConfigDict, SecretStr
from homecontrol_auth.schemas.users import UserPost
from homecontrol_base_api.types import StringUUID

class LoginPost(UserPost):
    """Schema for logging in"""
    
    long_lived: bool


class UserSession(BaseModel):
    """Schema for a user session"""
    
    model_config = ConfigDict(from_attributes=True)

    id: StringUUID
    user_id: StringUUID

class InternalUserSession(UserSession):
    """Schema for a user session for internal use only"""

    model_config = ConfigDict(from_attributes=True)

    access_token: SecretStr
    refresh_token: SecretStr
    long_lived: bool
    expiry_time: datetime