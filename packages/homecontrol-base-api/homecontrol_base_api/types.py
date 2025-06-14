from typing import Annotated, Union
from uuid import UUID

from pydantic import BeforeValidator

from homecontrol_base_api.exceptions import InvalidUUIDError


def convert_uuid_to_string(id: Union[UUID, str]):
    """Converts a UUID type to a string"""
    if isinstance(id, UUID):
        return str(id)
    else:
        return id


def convert_string_to_uuid(id: Union[UUID, str]):
    """Converts a string type to a UUID"""
    if isinstance(id, str):
        try:
            return UUID(id)
        except ValueError as exc:
            raise InvalidUUIDError(f"'{id}' is not a valid UUID") from exc
    else:
        return id


StringUUID = Annotated[str, BeforeValidator(convert_uuid_to_string)]
UUIDString = Annotated[UUID, BeforeValidator(convert_string_to_uuid)]
