import json
from pathlib import Path
from typing import Optional, Type, TypeVar
from pydantic import BaseModel, SecretStr
from pydantic.dataclasses import dataclass
from sqlalchemy import URL


class DatabaseSettings(BaseModel):
    """Setting required for connecting to a database"""

    driver: Optional[str] = None
    username: Optional[str] = None
    password: Optional[SecretStr] = None
    host: Optional[str] = None
    port: Optional[int] = None
    name: Optional[str] = None


def get_database_url(database_settings: DatabaseSettings) -> URL:
    return URL.create(
        drivername=database_settings.driver,
        username=database_settings.username,
        password=database_settings.password.get_secret_value() if database_settings.password is not None else None,
        host=database_settings.host,
        port=database_settings.port,
        database=database_settings.name,
    )
