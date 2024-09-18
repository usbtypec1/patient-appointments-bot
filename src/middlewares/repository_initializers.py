from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Update

from repositories.base import DatabaseRepository

__all__ = ('RepositoryInitializerMiddleware',)


class RepositoryInitializerMiddleware(BaseMiddleware):

    def __init__(self, **name_to_repository_class: type[DatabaseRepository]):
        self.__name_to_repository_class = name_to_repository_class

    async def __call__(
            self,
            handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: dict[str, Any],
    ):
        database_session = data['session']
        for name, repository_class in self.__name_to_repository_class.items():
            data[name] = repository_class(database_session)
        return await handler(event, data)
