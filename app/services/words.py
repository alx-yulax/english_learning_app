from sqlalchemy import select

from app.database.models import Word, User
from app.database.session import get_session


class WordsService:
    @staticmethod
    def add_word(
        user_id: int,
        english: str,
        translation: str,
        image_url: str | None = None,
        audio_path: str | None = None,
    ) -> Word:
        if not english or not translation:
            raise ValueError("english and translation are required")

        with get_session() as session:
            word = Word(
                user_id=user_id,
                english=english.strip(),
                translation=translation.strip(),
                image_url=image_url,
                audio_path=audio_path,
            )
            session.add(word)
            session.flush()

            return word

    @staticmethod
    def list_words(user_id: int) -> list[Word]:
        with get_session() as session:
            stmt = select(Word).where(Word.user_id == user_id).order_by(Word.id)
            return list(session.scalars(stmt))

    @staticmethod
    def list_words_by_telegram_id(telegram_id: int) -> list[Word]:
        with get_session() as session:
            user = (
                session.query(User)
                .filter(User.telegram_id == telegram_id)
                .first()
            )
            if not user:
                return []

            return (
                session.query(Word)
                .filter(Word.user_id == user.id)
                .order_by(Word.id)
                .all()
            )