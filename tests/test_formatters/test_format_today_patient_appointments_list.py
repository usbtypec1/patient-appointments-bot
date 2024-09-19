from datetime import date, datetime

import pytest

from formatters import format_today_patient_appointments_list
from models import PatientAppointmentDTO


def test_format_today_patient_appointments_list_no_appointments():
    patient_appointments = []

    result = format_today_patient_appointments_list(patient_appointments)

    expected_output = '😔 Сегодня нет пациентов'
    assert result == expected_output


def test_format_today_patient_appointments_list_one_appointment():
    patient_appointment = PatientAppointmentDTO(
        patient_full_name="John Doe",
        patient_born_on=date(1990, 4, 15),
        created_at=datetime(2023, 9, 19, 14, 30)
    )

    result = format_today_patient_appointments_list([patient_appointment])

    expected_output = (
        '<b>🗒️ Список пациентов сегодня</b>\n'
        '1. John Doe - 14:30'
    )
    assert result == expected_output


def test_format_today_patient_appointments_list_multiple_appointments():
    patient_appointments = [
        PatientAppointmentDTO(
            patient_full_name="John Doe",
            patient_born_on=date(1990, 4, 15),
            created_at=datetime(2023, 9, 19, 14, 30)
        ),
        PatientAppointmentDTO(
            patient_full_name="Jane Smith",
            patient_born_on=date(1985, 7, 22),
            created_at=datetime(2023, 9, 19, 15, 45)
        ),
    ]

    result = format_today_patient_appointments_list(patient_appointments)

    expected_output = (
        '<b>🗒️ Список пациентов сегодня</b>\n'
        '1. John Doe - 14:30\n'
        '2. Jane Smith - 15:45'
    )
    assert result == expected_output


if __name__ == '__main__':
    pytest.main()
