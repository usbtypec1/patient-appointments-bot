from datetime import date, datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base

__all__ = ('PatientAppointment',)


class PatientAppointment(Base):
    __tablename__ = 'patient_appointments'

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_full_name: Mapped[str]
    patient_born_on: Mapped[date]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    def __repr__(self):
        return (
            f'PatientAppointment('
            f'id={self.id!r}'
            f', patient_full_name={self.patient_full_name!r}'
            f', patient_born_on={self.patient_born_on!r}'
            f', created_at={self.created_at!r})'
        )
