from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

from homecontrol_base_api.config.core import DatabaseSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", env_nested_delimiter="__")

    # test: str
    database: DatabaseSettings = DatabaseSettings()


settings = Settings()
