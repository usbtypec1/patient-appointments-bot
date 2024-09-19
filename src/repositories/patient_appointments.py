from datetime import date, datetime

from sqlalchemy import func, select

from db.models import PatientAppointment
from logger import create_logger
from models import DailyPatientAppointmentsCountDTO, PatientAppointmentDTO
from repositories.base import DatabaseRepository

__all__ = ('PatientAppointmentRepository',)

logger = create_logger('repository')


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

    async def count_by_days(
            self,
            *,
            from_date: date,
            to_date: date,
    ):
        statement = (
            select(
                func.date(PatientAppointment.created_at),
                func.count('*'),
            )
            .where(
                PatientAppointment
                .created_at
                .between(from_date, to_date)
            )
            .group_by(func.date(PatientAppointment.created_at))
            .order_by(func.date(PatientAppointment.created_at))
        )

        result = await self._session.execute(statement)

        logger.debug(
            'Database query executed: count by days',
            extra={'result': result},
        )
        return [
            DailyPatientAppointmentsCountDTO(
                date=date,
                count=count,
            )
            for date, count in result
        ]
