import json
import logging.config
import pathlib
from typing import Final

__all__ = ('create_logger', 'setup_logging_from_config')

DEFAULT_LOGGING_CONFIG_FIL_PATH: Final[pathlib.Path] = (
        pathlib.Path(__file__).parent.parent / 'logging_config.default.json'
)


def create_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.propagate = False
    return logger


def setup_logging_from_config(
        config_file_path: pathlib.Path = DEFAULT_LOGGING_CONFIG_FIL_PATH,
) -> None:
    config_json = config_file_path.read_text(encoding='utf-8')
    config = json.loads(config_json)
    logging.config.dictConfig(config)
