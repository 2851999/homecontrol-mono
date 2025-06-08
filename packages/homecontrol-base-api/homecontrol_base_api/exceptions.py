import logging

from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

logger = logging.getLogger()


class BaseAPIError(Exception):
    """Base class for an API error"""

    status_code: int


class DatabaseError(BaseAPIError):
    """Base class for a database error"""


class DuplicateRecordError(DatabaseError):
    """Raised when attempting to insert a database record which has a duplicate unique key already in existence"""

    status_code = status.HTTP_409_CONFLICT


class RecordNotFoundError(DatabaseError):
    """Raised when attempting find a database record that doesn't exist"""

    status_code = status.HTTP_404_NOT_FOUND


class InvalidUUIDError(BaseAPIError):
    """Raised when attempting to convert an invalid string to a UUID"""

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


async def handle_base_api_error(_: Request, exc: BaseAPIError) -> JSONResponse:
    logger.exception(exc)
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"detail": str(exc)}),
    )
