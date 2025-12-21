from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.bot.handlers.states import AddWordState
from app.bot.keyboards.main import main_menu
from app.database.session import SessionLocal
from app.services.users import get_or_create_user
from app.services.words import create_word
from app.services.tts import generate_tts
from app.core.config import settings

from pathlib import Path
import uuid

router = Router()


@router.message(F.text == "➕ Добавить слово")
async def start_add_word(message: Message, state: FSMContext):
    await state.set_state(AddWordState.english)
    await message.answer("Введи слово / фразу / предложение на английском 🇬🇧")


@router.message(AddWordState.english, F.text)
async def add_english(message: Message, state: FSMContext):
    if len(message.text) > 500:
        await message.answer("Слишком длинный текст")
        return

    await state.update_data(english=message.text)
    await state.set_state(AddWordState.translation)
    await message.answer("Теперь введи перевод 🇷🇺")


@router.message(AddWordState.translation, F.text)
async def add_translation(message: Message, state: FSMContext):
    await state.update_data(translation=message.text)
    await state.set_state(AddWordState.image)
    await message.answer("Пришли картинку 🖼️ (или напиши 'нет')")


@router.message(AddWordState.image)
async def add_image(message: Message, state: FSMContext):
    data = await state.get_data()

    image_path = None
    audio_path = None

    media_dir = settings.MEDIA_PATH
    media_dir.mkdir(exist_ok=True)

    if message.photo:
        photo = message.photo[-1]
        filename = f"{uuid.uuid4()}.jpg"
        image_path = media_dir / filename
        await message.bot.download(photo.file_id, destination=image_path)

    # озвучка
    audio_filename = f"{uuid.uuid4()}.mp3"
    audio_path = media_dir / audio_filename
    generate_tts(data["english"], audio_path)

    with SessionLocal() as db:
        user = get_or_create_user(db, message.from_user.id)

        create_word(
            db=db,
            user_id=user.id,
            english=data["english"],
            translation=data["translation"],
            image_path=str(image_path) if image_path else None,
            audio_path=str(audio_path),
        )

    await state.clear()
    await message.answer(
        "✅ Слово добавлено и поставлено на повторение!",
        reply_markup=main_menu(),
    )
