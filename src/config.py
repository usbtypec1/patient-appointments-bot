from dataclasses import dataclass

from environs import Env

__all__ = ('Config', 'load_config_from_env_file')


@dataclass(frozen=True, slots=True)
class Config:
    telegram_bot_token: str


def load_config_from_env_file() -> Config:
    env = Env()
    env.read_env()

    telegram_bot_token: str = env.str('TELEGRAM_BOT_TOKEN')

    return Config(
        telegram_bot_token=telegram_bot_token,
    )
