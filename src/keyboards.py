from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

__all__ = ('MAIN_MENU_REPLY_MARKUP',)

MAIN_MENU_REPLY_MARKUP = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Добавить пациента'),
        ],
        [
            KeyboardButton(text='Сегодня'),
            KeyboardButton(text='Текущая неделя'),
        ],
    ],
    resize_keyboard=True,
)
