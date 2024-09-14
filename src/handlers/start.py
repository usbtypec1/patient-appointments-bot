from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message

router = Router(name=__name__)


@router.message(
    CommandStart(),
    StateFilter('*'),
)
async def on_start(message: Message) -> None:
    await message.answer()
