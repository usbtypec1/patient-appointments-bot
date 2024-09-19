import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import (
    AsyncEngine, async_sessionmaker,
    create_async_engine,
)

import handlers
from config import load_config_from_env_file
from db.base import create_tables
from logger import create_logger, setup_logging_from_config
from middlewares import (
    DatabaseSessionMiddleware,
    RepositoryInitializerMiddleware,
)
from repositories.patient_appointments import PatientAppointmentRepository

logger = create_logger('app')


async def on_shutdown(engine: AsyncEngine):
    await engine.dispose()


def include_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.include_routers(
        handlers.start.router,
        handlers.patients_today.router,
        handlers.weekly_patients.router,
        handlers.add_patient.router,
    )
    logger.info('Handlers set up')


async def main() -> None:
    config = load_config_from_env_file()

    setup_logging_from_config()

    engine = create_async_engine(config.database.dsn)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    await create_tables(engine)

    default_bot_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)
    bot = Bot(
        token=config.telegram_bot_token,
        default=default_bot_properties,
    )

    redis = Redis(
        host=config.redis.host,
        port=config.redis.port,
    )
    storage = RedisStorage(redis=redis)

    dispatcher = Dispatcher(storage=storage)

    dispatcher.shutdown.register(on_shutdown)

    database_session_middleware = DatabaseSessionMiddleware(session_factory)
    dispatcher.update.middleware(database_session_middleware)

    repository_factories_middleware = RepositoryInitializerMiddleware(
        patient_appointment_repository=PatientAppointmentRepository,
    )
    dispatcher.update.middleware(repository_factories_middleware)

    include_handlers(dispatcher)

    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
