import asyncio
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.services.repetition import get_due_repetitions
from app.bot.keyboards.repeat import repeat_keyboard

async def repetition_scheduler(bot):
    while True:
        await asyncio.sleep(60)

        with SessionLocal() as db:
            repetitions = get_due_repetitions(db)

            for repetition in repetitions:
                user = repetition.word.user

                await bot.send_message(
                    user.telegram_id,
                    "⏰ Пора повторить слова!",
                    reply_markup=repeat_keyboard(),
                )
