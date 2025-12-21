import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.core.config import settings
from app.bot.handlers import router as add_word_router
from app.bot.keyboards.main import main_menu
from app.core.scheduler import repetition_scheduler


async def main():
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )

    dp = Dispatcher()
    dp.include_router(add_word_router)

    asyncio.create_task(repetition_scheduler(bot))

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
