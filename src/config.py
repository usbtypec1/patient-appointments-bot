from dataclasses import dataclass

from environs import Env

__all__ = (
    'Config',
    'DatabaseConfig',
    'RedisConfig',
    'load_config_from_env_file',
)


@dataclass(frozen=True, slots=True)
class DatabaseConfig:
    name: str
    port: int
    host: str
    user: str
    password: str

    @property
    def dsn(self) -> str:
        return (
            f'postgresql+asyncpg://{self.user}:{self.password}'
            f'@{self.host}:{self.port}/{self.name}'
        )


@dataclass(frozen=True, slots=True)
class RedisConfig:
    host: str
    port: int


@dataclass(frozen=True, slots=True)
class Config:
    telegram_bot_token: str
    database: DatabaseConfig
    redis: RedisConfig


def load_config_from_env_file() -> Config:
    env = Env()
    env.read_env()

    telegram_bot_token: str = env.str('TELEGRAM_BOT_TOKEN')

    database = DatabaseConfig(
        host=env.str('POSTGRES_HOST', default='postgres'),
        port=env.int('POSTGRES_PORT', default=5432),
        name=env.str('POSTGRES_DB'),
        user=env.str('POSTGRES_USER'),
        password=env.str('POSTGRES_PASSWORD'),
    )

    redis = RedisConfig(
        host=env.str('REDIS_HOST'),
        port=env.int('REDIS_PORT'),
    )

    return Config(
        telegram_bot_token=telegram_bot_token,
        database=database,
        redis=redis,
    )
