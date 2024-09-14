import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import handlers
from config import load_config_from_env_file


def include_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.include_routers(
        handlers.patients.router,
    )


async def main() -> None:
    config = load_config_from_env_file()

    default_bot_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)
    bot = Bot(
        token=config.telegram_bot_token,
        default=default_bot_properties,
    )
    dispatcher = Dispatcher()

    include_handlers(dispatcher)

    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
