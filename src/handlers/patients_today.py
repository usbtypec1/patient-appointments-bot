from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from formatters import format_today_patient_appointments_list
from repositories.patient_appointments import PatientAppointmentRepository
from services import PatientAppointmentsService

__all__ = ('router',)
router = Router(name=__name__)


@router.message(
    F.text == 'Пациенты сегодня',
    StateFilter('*'),
)
async def on_show_patients_today_list(
        message: Message,
        patient_appointment_repository: PatientAppointmentRepository,
        state: FSMContext,
) -> None:
    await state.clear()
    service = PatientAppointmentsService(patient_appointment_repository)
    patient_appointments = await service.get_today_patient_appointments()
    text = format_today_patient_appointments_list(patient_appointments)
    await message.answer(text)
