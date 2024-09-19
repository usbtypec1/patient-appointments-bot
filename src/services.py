import string
from datetime import date, datetime, timedelta

from exceptions import (
    InvalidBirthDateError,
    PatientNameContainsPunctuationError,
    PatientTooOldError,
)
from models import (
    DailyPatientAppointmentsCountDTO,
    PatientAppointmentDTO,
    Period,
)
from repositories.patient_appointments import PatientAppointmentRepository

__all__ = (
    'contains_punctuation',
    'validate_age',
    'PatientAppointmentsService',
    'parse_date',
    'validate_full_name',
)


def get_current_week_period() -> Period:
    today = datetime.utcnow().today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return Period(start=start_of_week.date(), end=end_of_week.date())


def contains_punctuation(text: str) -> bool:
    return any(char in text for char in string.punctuation)


def parse_date(date_string: str) -> datetime:
    """
    Parse date string in format 'DD.MM.YYYY'.

    Args:
        date_string:

    Returns:
        datetime object.

    Raises:
        InvalidBirthDateError: if date_string has invalid format.
    """
    try:
        return datetime.strptime(date_string, '%d.%m.%Y')
    except ValueError:
        raise InvalidBirthDateError


def is_older_than(birth_date: datetime, lifetime: timedelta) -> bool:
    now = datetime.now()
    return (now - birth_date) > lifetime


def validate_age(birth_date: datetime) -> None:
    max_age_in_years = 100
    lifetime = timedelta(days=365 * max_age_in_years)
    if is_older_than(birth_date, lifetime):
        raise PatientTooOldError(max_age_in_years=max_age_in_years)


def validate_full_name(full_name: str) -> None:
    if contains_punctuation(full_name):
        raise PatientNameContainsPunctuationError


class PatientAppointmentsService:

    def __init__(self, repository: PatientAppointmentRepository):
        self.__repository = repository

    async def create_patient_appointment(
            self,
            *,
            patient_full_name: str,
            patient_born_on: date,
    ) -> PatientAppointmentDTO:
        """
        Create a new patient appointment.

        Keyword Args:
            patient_full_name: patient's full name.
            patient_born_on: patient's birth date.

        Returns:
            PatientAppointmentDTO object.

        Raises:
            PatientNameContainsPunctuation: if patient_full_name
                                            contains punctuation.
            PatientTooOldError: if patient_born_on is older than 100 years.
        """
        return await self.__repository.create(
            patient_full_name=patient_full_name,
            patient_born_on=patient_born_on,
        )

    async def get_today_patient_appointments(
            self,
    ) -> list[PatientAppointmentDTO]:
        now = datetime.utcnow()
        from_datetime = datetime(
            year=now.year,
            month=now.month,
            day=now.day,
        )
        to_datetime = datetime(
            year=now.year,
            month=now.month,
            day=now.day,
            hour=23,
            minute=59,
            second=59,
        )
        return await self.__repository.get_created_at_between(
            from_datetime=from_datetime,
            to_datetime=to_datetime,
        )

    async def get_appointments_count_for_current_week(
            self,
    ) -> list[DailyPatientAppointmentsCountDTO]:
        period = get_current_week_period()
        return await self.__repository.count_by_days(
            from_date=period.start,
            to_date=period.end,
        )
