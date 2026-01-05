from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import (
    Message
)

from app.core.config import get_settings
from app.services.users import UsersService
from app.bot.keyboards.main import main_keyboard

router = Router()
settings = get_settings()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    """
    Обработчик команды /start (aiogram 3).
    Создаёт пользователя в БД и показывает клавиатуру с WebApp.
    """

    user = UsersService.get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
    )

    await message.answer(
        f"Привет, {user.first_name or 'друг'} 👋\n"
        "Готов учить английские слова1?",
        reply_markup=main_keyboard(),
    )
