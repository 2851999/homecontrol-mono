from typing import Optional

from pydantic import BaseModel

# -------------------- Post response from a Hue Bridge's /api endpoint --------------------


class HueBridgeAPIPostResponseSuccess(BaseModel):
    username: str
    clientkey: str


class HueBridgeAPIPostResponseError(BaseModel):
    type: int
    address: str
    description: str


class HueBridgeAPIPostResponse(BaseModel):

    success: Optional[HueBridgeAPIPostResponseSuccess] = None
    error: Optional[HueBridgeAPIPostResponseError] = None
