from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.database.models import Repetition

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


def get_due_repetitions(db: Session) -> list[Repetition]:
    now = datetime.utcnow()
    return (
        db.query(Repetition)
        .filter(Repetition.next_repeat_at <= now)
        .all()
    )


def mark_result(
    db: Session,
    repetition: Repetition,
    remembered: bool,
) -> None:
    now = datetime.utcnow()

    if remembered:
        repetition.level = min(repetition.level + 1, len(INTERVALS) - 1)
        repetition.last_result = "remember"
    else:
        repetition.level = 0
        repetition.last_result = "forgot"

    repetition.next_repeat_at = now + INTERVALS[repetition.level]
    db.commit()
