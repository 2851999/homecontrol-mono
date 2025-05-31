from homecontrol_base_api.config.core import DatabaseSettings
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class MideaSettings(BaseModel):

    username: str
    password: SecretStr


class Settings(BaseSettings):
    """Settings of homecontrol-auth"""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", env_nested_delimiter="__")

    database: DatabaseSettings = DatabaseSettings()
    midea: MideaSettings


settings = Settings()
