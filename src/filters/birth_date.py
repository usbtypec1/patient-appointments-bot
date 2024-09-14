from datetime import datetime

from aiogram.types import Message

__all__ = (
    'lifetime_less_than_hundred_years_filter',
    'birth_date_valid_format_filter',
)


def lifetime_less_than_hundred_years_filter(
        message: Message,
        born_on: datetime,
) -> bool:
    lifetime = datetime.utcnow() - born_on
    threshold_in_seconds = 365 * 100 * 24 * 60 * 60
    return lifetime.total_seconds() < threshold_in_seconds


def birth_date_valid_format_filter(message: Message) -> dict | bool:
    try:
        born_on = datetime.strptime(message.text, '%d.%m.%Y')
    except ValueError:
        return False

    return {'born_on': born_on}
