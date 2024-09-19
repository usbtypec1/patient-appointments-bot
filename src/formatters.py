from collections.abc import Iterable

from models import DailyPatientAppointmentsCountDTO, PatientAppointmentDTO

__all__ = (
    'format_patient_appointment_created',
    'format_today_patient_appointments_list',
    'format_weekly_appointments_count',
)

weekday_names = {
    1: 'Понедельник',
    2: 'Вторник',
    3: 'Среда',
    4: 'Четверг',
    5: 'Пятница',
    6: 'Суббота',
    7: 'Воскресенье',
}


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


def format_weekly_appointments_count(
        weekly_appointments_count: Iterable[DailyPatientAppointmentsCountDTO],
) -> str:
    weekly_appointments_count = tuple(weekly_appointments_count)

    if not weekly_appointments_count:
        return '😔 На этой неделе нет пациентов'

    lines: list[str] = ['<b>📊 Количество пациентов на этой неделе:</b>']

    for daily_appointments_count in weekly_appointments_count:
        weekday_name = weekday_names[daily_appointments_count.date.isoweekday()]
        lines.append(
            f'{weekday_name} ({daily_appointments_count.date:%d.%m.%Y}):'
            f' {daily_appointments_count.count} пациент(ов)'
        )

    return '\n'.join(lines)
