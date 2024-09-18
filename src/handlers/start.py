from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards import MAIN_MENU_REPLY_MARKUP

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    CommandStart(),
    StateFilter('*'),
)
async def on_start(message: Message, state: FSMContext) -> None:
    await message.answer(
        text='Главное меню',
        reply_markup=MAIN_MENU_REPLY_MARKUP,
    )
    await state.clear()
