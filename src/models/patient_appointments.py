from datetime import date, datetime

from pydantic import BaseModel

__all__ = ('PatientAppointmentDTO', 'DailyPatientAppointmentsCountDTO')


class PatientAppointmentDTO(BaseModel):
    patient_full_name: str
    patient_born_on: date
    created_at: datetime


class DailyPatientAppointmentsCountDTO(BaseModel):
    date: date
    count: int
