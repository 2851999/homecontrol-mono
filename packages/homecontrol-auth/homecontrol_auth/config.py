from homecontrol_base_api.config.core import DatabaseSettings
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings of homecontrol-auth"""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", env_nested_delimiter="__")

    database: DatabaseSettings = DatabaseSettings()
    secret_key: SecretStr
    access_token_expiry_seconds: int
    refresh_token_expiry_seconds: int
    long_lived_refresh_token_expiry_seconds: int


settings = Settings()
