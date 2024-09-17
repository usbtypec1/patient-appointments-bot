from datetime import date, datetime

from pydantic import BaseModel

__all__ = ('PatientAppointmentDTO',)


class PatientAppointmentDTO(BaseModel):
    patient_full_name: str
    patient_born_on: date
    created_at: datetime
