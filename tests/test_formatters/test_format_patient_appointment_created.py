from formatters import format_patient_appointment_created
from models import PatientAppointmentDTO


def test_format_patient_appointment_created():
    patient_appointment = PatientAppointmentDTO.model_validate({
        'patient_full_name': 'John',
        'patient_born_on': '1990-04-15',
        'created_at': '2021-10-10T10:00:00',
    })

    result = format_patient_appointment_created(patient_appointment)

    expected_output = (
        '✅ Пациент <b>John</b> успешно добавлен.\n'
        'Дата рождения: 15.04.1990'
    )
    assert result == expected_output
