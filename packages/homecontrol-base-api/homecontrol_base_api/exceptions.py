from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


class BaseAPIError(Exception):
    """Base class for an API error"""

    status_code: int


class DatabaseError(BaseAPIError):
    """Base class for a database error"""


class DuplicateRecordError(DatabaseError):
    """Raised when attempting to insert a database record which has a duplicate unique key already in existence"""

    status_code = status.HTTP_409_CONFLICT


class NoRecordFound(DatabaseError):
    """Raised when attempting find a database record that doesn't exist"""

    status_code = status.HTTP_404_NOT_FOUND


def handle_base_api_error(_: Request, exc: BaseAPIError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"detail": str(exc)}),
    )
