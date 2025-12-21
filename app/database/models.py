from datetime import datetime
from sqlalchemy import (
    String,
    Integer,
    DateTime,
    ForeignKey,
    Text,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(
        unique=True,
        index=True,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    words = relationship(
        "Word",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Word(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    english_text: Mapped[str] = mapped_column(Text, nullable=False)
    translation: Mapped[str] = mapped_column(Text, nullable=False)

    image_path: Mapped[str | None] = mapped_column(String(255))
    audio_path: Mapped[str | None] = mapped_column(String(255))

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    user = relationship("User", back_populates="words")
    repetition = relationship(
        "Repetition",
        back_populates="word",
        uselist=False,
        cascade="all, delete-orphan",
    )


Index("ix_words_user_text", Word.user_id, Word.english_text)


class Repetition(Base):
    __tablename__ = "repetitions"

    id: Mapped[int] = mapped_column(primary_key=True)
    word_id: Mapped[int] = mapped_column(
        ForeignKey("words.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    level: Mapped[int] = mapped_column(Integer, default=0)
    next_repeat_at: Mapped[datetime] = mapped_column(
        DateTime,
        index=True,
        nullable=False,
    )

    last_result: Mapped[str | None] = mapped_column(String(20))

    word = relationship("Word", back_populates="repetition")
