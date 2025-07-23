from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    api_key: SecretStr = Field(alias="DEEPSEEK_API_KEY")


config = Config()
