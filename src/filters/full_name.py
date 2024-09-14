import string

from aiogram.types import Message

__all__ = ('message_text_contains_punctuation_filter',)


def message_text_contains_punctuation_filter(message: Message) -> bool:
    return any(
        punctuation_character in message.text
        for punctuation_character in string.punctuation
    )
