from datetime import date, datetime

from pydantic import TypeAdapter
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
    ):
        patient_appointment = PatientAppointment(
            patient_full_name=patient_full_name,
            patient_born_on=patient_born_on,
        )
        self._session.add(patient_appointment)
        await self._session.commit()

    async def get_created_at_between(
            self,
            *,
            from_datetime: datetime,
            to_datetime: datetime,
    ) -> tuple[PatientAppointmentDTO, ...]:
        statement = (
            select(PatientAppointment)
            .where(
                PatientAppointment
                .created_at
                .between(from_datetime, to_datetime)
            )
        )
        patient_appointments = await self._session.scalars(statement)

        type_adapter = TypeAdapter(tuple[PatientAppointmentDTO, ...])
        return type_adapter.validate_python(patient_appointments)
