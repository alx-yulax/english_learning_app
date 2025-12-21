from app.database.base import Base
from app.database.session import engine
from app.database import models  # noqa: F401


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
