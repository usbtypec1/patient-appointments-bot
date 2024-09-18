from datetime import date, datetime

from sqlalchemy import select

from db.models import PatientAppointment
from models import PatientAppointmentDTO
from repositories.base import DatabaseRepository

__all__ = ('PatientAppointmentRepository',)


class PatientAppointmentRepository(DatabaseRepository):

    async def create(
            self,
            *,
            patient_full_name: str,
            patient_born_on: date,
    ) -> PatientAppointmentDTO:
        patient_appointment = PatientAppointment(
            patient_full_name=patient_full_name,
            patient_born_on=patient_born_on,
        )
        self._session.add(patient_appointment)
        await self._session.commit()

        return PatientAppointmentDTO(
            patient_full_name=patient_appointment.patient_full_name,
            patient_born_on=patient_appointment.patient_born_on,
            created_at=patient_appointment.created_at,
        )

    async def get_created_at_between(
            self,
            *,
            from_datetime: datetime,
            to_datetime: datetime,
    ) -> list[PatientAppointmentDTO]:
        statement = (
            select(PatientAppointment)
            .where(
                PatientAppointment
                .created_at
                .between(from_datetime, to_datetime)
            )
        )
        patient_appointments = await self._session.scalars(statement)

        return [
            PatientAppointmentDTO(
                patient_full_name=patient_appointment.patient_full_name,
                patient_born_on=patient_appointment.patient_born_on,
                created_at=patient_appointment.created_at,
            )
            for patient_appointment in patient_appointments
        ]
