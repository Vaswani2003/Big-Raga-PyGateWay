import logging
from typing import Union
from functools import lru_cache
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = '.env',
        env_file_encoding = 'utf-8',
        extra = 'ignore'
    )

class CoreSettings(AppBaseSettings):
    HOST_IP: str = '0.0.0.0'
    PORT : int = 8000

class LoggerConfig(AppBaseSettings):
    LEVEL: Union[int, str]  = logging.DEBUG
    FILE_NAME: str = "app.log"

    @field_validator("LEVEL", mode="before")
    @classmethod
    def normalize_log_level(cls, value):
        if isinstance(value, str):
            value = value.upper()
            if hasattr(logging, value):
                return getattr(logging, value)

        try:
            value = int(value)
        except Exception:
            raise ValueError("Invalid LOG_LEVEL")

        if value <= 10:
            return logging.DEBUG

        elif value <= 20:
            return logging.INFO

        elif value <= 30:
            return logging.WARNING

        elif value <= 40:
            return logging.ERROR

        else:
            return logging.CRITICAL


@lru_cache(maxsize=4)
def get_logger_config():
    return LoggerConfig()

@lru_cache(maxsize=4)
def get_core_settings():
    return CoreSettings()
