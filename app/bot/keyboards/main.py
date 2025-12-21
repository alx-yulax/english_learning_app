from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Добавить слово")],
            [KeyboardButton(text="🔁 Повторить слова")],
        ],
        resize_keyboard=True,
    )
