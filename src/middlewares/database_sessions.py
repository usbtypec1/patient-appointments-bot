from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Update
from sqlalchemy.ext.asyncio import async_sessionmaker

__all__ = ('DatabaseSessionMiddleware',)


class DatabaseSessionMiddleware(BaseMiddleware):

    def __init__(self, session_factory: async_sessionmaker):
        self.__session_factory = session_factory

    async def __call__(
            self,
            handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: dict[str, Any],
    ):
        async with self.__session_factory() as session:
            data['session'] = session
            return await handler(event, data)
