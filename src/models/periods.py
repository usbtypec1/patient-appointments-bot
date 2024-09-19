from datetime import date

from pydantic import BaseModel

__all__ = ('Period',)


class Period(BaseModel):
    start: date
    end: date
