from sqlalchemy.orm import Session

from app.database.models import User


def get_or_create_user(db: Session, telegram_id: int) -> User:
    user = (
        db.query(User)
        .filter(User.telegram_id == telegram_id)
        .one_or_none()
    )
    if user:
        return user

    user = User(telegram_id=telegram_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
