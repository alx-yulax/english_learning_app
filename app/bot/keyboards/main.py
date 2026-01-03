from aiogram.types import InlineKeyboardMarkup, WebAppInfo, InlineKeyboardButton


def main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="OPEN WEBAPP",
                    web_app=WebAppInfo(
                        url="https://english-web-app.yulax.ru/webapp/"
                    ),
                )
            ]
        ]
    )
