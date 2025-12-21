from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings
from contextlib import contextmanager

settings = get_settings()

engine = create_engine(
    settings.DATABASE_URL,
    echo=(settings.ENV == "development"),
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()