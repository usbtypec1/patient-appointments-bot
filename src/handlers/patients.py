from datetime import datetime

from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import StateFilter, invert_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from filters import (
    birth_date_valid_format_filter, lifetime_less_than_hundred_years_filter,
    message_text_contains_punctuation_filter,
)
from states import PatientAddStates

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text,
    F.chat.type == ChatType.PRIVATE,
    birth_date_valid_format_filter,
    lifetime_less_than_hundred_years_filter,
    StateFilter(PatientAddStates.born_on),
)
async def on_patient_birth_date_enter(
        message: Message,
        state: FSMContext,
        born_on: datetime,
) -> None:
    state_data = await state.get_data()
    full_name: str = state_data['full_name']
    print(full_name, born_on)
    await state.clear()


@router.message(
    F.text,
    F.chat.type == ChatType.PRIVATE,
    invert_f(birth_date_valid_format_filter),
    StateFilter(PatientAddStates.born_on),
)
async def on_patient_birth_date_invalid(message: Message) -> None:
    await message.reply(
        '❌ Неверный формат даты рождения.'
        ' Введите еще раз в формате ДД.ММ.ГГГГ'
    )


@router.message(
    F.text,
    F.chat.type == ChatType.PRIVATE,
    birth_date_valid_format_filter,
    invert_f(lifetime_less_than_hundred_years_filter),
    StateFilter(PatientAddStates.born_on),
)
async def on_lifetime_greater_than_hundred_years(message: Message) -> None:
    await message.reply('❌ Возраст пациента не должен превышать 100 лет')


@router.message(
    F.text,
    F.chat.type == ChatType.PRIVATE,
    message_text_contains_punctuation_filter,
    StateFilter(PatientAddStates.full_name),
)
async def on_patient_full_name_enter(
        message: Message,
) -> None:
    await message.reply('❌ ФИО не должно содержать спецсимволов')


@router.message(
    F.text,
    F.chat.type == ChatType.PRIVATE,
    invert_f(message_text_contains_punctuation_filter),
    StateFilter(PatientAddStates.full_name),
)
async def on_patient_full_name_enter(
        message: Message,
        state: FSMContext,
) -> None:
    await state.update_data(full_name=message.text)
    await state.set_state(PatientAddStates.born_on)
    await message.reply('Введите дату рождения пациента в формате ДД.ММ.ГГГГ')


@router.message(
    F.text == 'Добавить пациента',
    F.chat.type == ChatType.PRIVATE,
    StateFilter('*'),
)
async def on_start_patient_add_flow(
        message: Message,
        state: FSMContext,
) -> None:
    await state.set_state(PatientAddStates.full_name)
    await message.reply('Введите ФИО пациента')
