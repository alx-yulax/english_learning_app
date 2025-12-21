from aiogram import Router, F
from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    WebAppInfo,
)

from app.core.config import get_settings
from app.services.users import UsersService
from app.bot.keyboards.main import main_keyboard

router = Router()
settings = get_settings()


@router.message(F.text == "/start")
async def start_handler(message: Message) -> None:
    """
    Обработчик команды /start (aiogram 3).
    Создаёт пользователя в БД и показывает основную клавиатуру.
    """
    user = UsersService.get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
    )

    await message.answer(
        f"Привет, {user.first_name or 'друг'} 👋\n"
        "Готов учить английские слова?",
        reply_markup=main_keyboard(),
    )


@router.message(F.text == "📚 Учить слова")
async def open_webapp(message: Message) -> None:
    """
    Открывает Telegram Web App.
    """
    await message.answer(
        "Открываю учебник 📖",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text="Открыть WebApp",
                        web_app=WebAppInfo(url=settings.WEBAPP_BASE_URL),
                    )
                ]
            ],
            resize_keyboard=True,
        ),
    )
