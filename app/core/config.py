from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class CoreSettings(BaseSettings):
    HOST_IP: str = '0.0.0.0'
    PORT : int = 8000

    model_config = SettingsConfigDict(
        env_file = '.env',
        env_file_encoding = 'utf-8',
        extra = 'ignore'
    )

@lru_cache(maxsize=4)
def get_core_settings():
    return CoreSettings()
