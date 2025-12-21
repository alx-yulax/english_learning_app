import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from app.core.config import get_settings
from app.bot.handlers.start import router as start_router


async def main():
    settings = get_settings()

    bot = Bot(
        token=settings.BOT_TOKEN,
        default={"parse_mode": ParseMode.HTML},
    )

    dp = Dispatcher()
    dp.include_router(start_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
