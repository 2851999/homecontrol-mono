from pydantic import BaseModel, SecretStr
from sqlalchemy import URL


class DatabaseSettings(BaseModel):
    """Setting required for connecting to a database"""

    driver: str | None = None
    username: str | None = None
    password: SecretStr | None = None
    host: str | None = None
    port: int | None = None
    name: str | None = None


def get_database_url(database_settings: DatabaseSettings) -> URL:
    return URL.create(
        drivername=database_settings.driver,
        username=database_settings.username,
        password=database_settings.password.get_secret_value() if database_settings.password is not None else None,
        host=database_settings.host,
        port=database_settings.port,
        database=database_settings.name,
    )
