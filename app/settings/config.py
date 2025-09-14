import logging
import os
import pprint
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from settings.base import PydanticBaseSettings, BASE_DIR

logger = logging.getLogger(__name__)

CONFIG_PATH = Path(os.environ.get("CONFIG", BASE_DIR.parent / "config.yaml"))


class LogConfig(BaseSettings):
    path: Path = BASE_DIR / "logs"
    console_format: str = Field(
        default="%(levelname)s %(asctime)s %(name)s %(module)s %(funcName)s %(lineno)d: %(message)s"
    )
    file_format: str = Field(
        default="%(levelname)s %(asctime)s %(name)s %(module)s %(funcName)s %(lineno)d: %(message)s"
    )


class PromptConfig(BaseSettings):
    system_prompt: str = Field(default="")


class Config(PydanticBaseSettings):
    model_config = SettingsConfigDict(
        yaml_file=CONFIG_PATH,
        env_file=".env",
        env_file_encoding="utf-8",
    )

    prompt: PromptConfig = PromptConfig()

    log: LogConfig = LogConfig()


config = Config()

def print_config():
    logger.debug(f'{CONFIG_PATH=}')
    lines = pprint.pformat(
        config.model_dump(),
        indent=2,
    ).split('\n')
    for line in lines:
        logger.debug(line)