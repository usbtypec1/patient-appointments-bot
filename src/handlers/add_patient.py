from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from exceptions import (
    InvalidBirthDateError,
    PatientNameContainsPunctuationError,
    PatientTooOldError,
)
from formatters import format_patient_appointment_created
from logger import create_logger
from repositories.patient_appointments import PatientAppointmentRepository
from services import (
    PatientAppointmentsService,
    parse_date,
    validate_age,
    validate_full_name,
)
from states import PatientAddStates

__all__ = ('router',)

logger = create_logger('event_handlers')

router = Router(name=__name__)


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


@router.message(
    F.text,
    F.chat.type == ChatType.PRIVATE,
    StateFilter(PatientAddStates.born_on),
)
async def on_patient_birth_date_enter(
        message: Message,
        state: FSMContext,
        patient_appointment_repository: PatientAppointmentRepository,
) -> None:
    try:
        born_on = parse_date(message.text)
    except InvalidBirthDateError:
        await message.reply(
            'Неверный формат даты рождения.'
            ' Введите её в формате DD.MM.YYYY'
        )
        return
    try:
        validate_age(born_on)
    except PatientTooOldError as error:
        await message.reply(
            f'Возраст пациента не может быть больше {error.max_age_in_years}',
        )
        return

    state_data = await state.get_data()
    full_name: str = state_data['full_name']
    await state.clear()

    service = PatientAppointmentsService(patient_appointment_repository)
    patient_appointment = await service.create_patient_appointment(
        patient_full_name=full_name,
        patient_born_on=born_on,
    )

    await message.reply(format_patient_appointment_created(patient_appointment))


@router.message(
    F.text,
    F.chat.type == ChatType.PRIVATE,
    StateFilter(PatientAddStates.full_name),
)
async def on_patient_full_name_enter(
        message: Message,
        state: FSMContext,
) -> None:
    try:
        validate_full_name(message.text)
    except PatientNameContainsPunctuationError:
        await message.reply('ФИО не должно содержать знаки пунктуации')
        return
    await state.update_data(full_name=message.text)
    await state.set_state(PatientAddStates.born_on)
    await message.reply('Введите дату рождения пациента в формате ДД.ММ.ГГГГ')
