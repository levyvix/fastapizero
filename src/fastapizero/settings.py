import os

from pydantic_settings import BaseSettings, SettingsConfigDict

dot_env_path = os.path.join(os.path.dirname(__file__), '.env')


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=dot_env_path,
        env_file_encoding='utf-8',
    )

    DATABASE_URL: str
