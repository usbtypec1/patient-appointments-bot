from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from formatters import format_weekly_appointments_count
from repositories.patient_appointments import PatientAppointmentRepository
from services import PatientAppointmentsService

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text == 'Текущая неделя',
    StateFilter('*'),
)
async def on_show_weekly_patients(
        message: Message,
        patient_appointment_repository: PatientAppointmentRepository,
) -> None:
    service = PatientAppointmentsService(patient_appointment_repository)
    appointments_count = await service.get_appointments_count_for_current_week()
    text = format_weekly_appointments_count(appointments_count)
    await message.answer(text)
