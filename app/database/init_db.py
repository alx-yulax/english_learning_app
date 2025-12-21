from app.database.base import Base
from app.database.session import engine

# импорт моделей ОБЯЗАТЕЛЕН
from app.database.models import User, Word  # noqa


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
