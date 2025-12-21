from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.bot.keyboards.repeat import repeat_keyboard

def repeat_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔁 Повторить слова",
                    web_app={"url": "https://english-web-app.yulax.ru/webapp"},
                )
            ]
        ]
    )
