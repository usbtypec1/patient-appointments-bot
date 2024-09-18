from collections.abc import Iterable

from models import PatientAppointmentDTO

__all__ = (
    'format_patient_appointment_created',
    'format_today_patient_appointments_list',
)


def format_patient_appointment_created(
        patient_appointment: PatientAppointmentDTO,
) -> str:
    return (
        f'✅ Пациент <b>{patient_appointment.patient_full_name}</b>'
        f' успешно добавлен.\n'
        f'Дата рождения: {patient_appointment.patient_born_on:%d.%m.%Y}'
    )


def format_today_patient_appointments_list(
        patient_appointments: Iterable[PatientAppointmentDTO],
) -> str:
    patient_appointments = tuple(patient_appointments)

    if not patient_appointments:
        return '😔 Сегодня нет пациентов'

    lines: list[str] = ['<b>🗒️ Список пациентов сегодня</b>']

    for number, patient_appointment in enumerate(patient_appointments, start=1):
        lines.append(
            f'{number}. {patient_appointment.patient_full_name}'
            f' - {patient_appointment.created_at:%H:%M}'
        )

    return '\n'.join(lines)
