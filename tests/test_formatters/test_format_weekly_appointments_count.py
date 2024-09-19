from datetime import date

import pytest

from formatters import format_weekly_appointments_count
from models import DailyPatientAppointmentsCountDTO


def test_format_weekly_appointments_count_no_appointments():
    weekly_appointments_count = []

    result = format_weekly_appointments_count(weekly_appointments_count)

    expected_output = '😔 На этой неделе нет пациентов'
    assert result == expected_output


def test_format_weekly_appointments_count_one_day():
    weekly_appointments_count = [
        DailyPatientAppointmentsCountDTO(
            date=date(2023, 9, 18),  # Monday
            count=5
        )
    ]

    result = format_weekly_appointments_count(weekly_appointments_count)

    expected_output = (
        '<b>📊 Количество пациентов на этой неделе:</b>\n'
        'Понедельник (18.09.2023): 5 пациент(ов)'
    )
    assert result == expected_output


def test_format_weekly_appointments_count_multiple_days():
    weekly_appointments_count = [
        DailyPatientAppointmentsCountDTO(
            date=date(2023, 9, 18),
            count=5
        ),
        DailyPatientAppointmentsCountDTO(
            date=date(2023, 9, 20),
            count=3
        ),
        DailyPatientAppointmentsCountDTO(
            date=date(2023, 9, 22),
            count=7
        )
    ]

    result = format_weekly_appointments_count(weekly_appointments_count)

    expected_output = (
        '<b>📊 Количество пациентов на этой неделе:</b>\n'
        'Понедельник (18.09.2023): 5 пациент(ов)\n'
        'Среда (20.09.2023): 3 пациент(ов)\n'
        'Пятница (22.09.2023): 7 пациент(ов)'
    )
    assert result == expected_output


if __name__ == '__main__':
    pytest.main()
