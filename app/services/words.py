from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.database.models import Word, Repetition

INTERVALS = [
    timedelta(minutes=20),
    timedelta(hours=1),
    timedelta(hours=2),
    timedelta(hours=4),
    timedelta(hours=8),
    timedelta(days=1),
    timedelta(days=2),
    timedelta(days=4),
    timedelta(days=8),
    timedelta(days=16),
    timedelta(days=32),
    timedelta(days=64),
]


def create_word(
    db: Session,
    user_id: int,
    english: str,
    translation: str,
    image_path: str | None,
    audio_path: str | None,
) -> Word:
    now = datetime.utcnow()

    word = Word(
        user_id=user_id,
        english_text=english.strip(),
        translation=translation.strip(),
        image_path=image_path,
        audio_path=audio_path,
    )
    db.add(word)
    db.flush()

    repetition = Repetition(
        word_id=word.id,
        level=0,
        next_repeat_at=now + INTERVALS[0],
        last_result=None,
    )
    db.add(repetition)

    db.commit()
    db.refresh(word)
    return word
