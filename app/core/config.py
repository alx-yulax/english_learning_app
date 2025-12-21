from pathlib import Path
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os


# Загружаем .env из корня проекта
BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)


class Settings(BaseModel):
    # Environment
    ENV: str = Field(default="development")

    # Database
    DATABASE_URL: str

    # Telegram
    BOT_TOKEN: str

    # Flask
    SECRET_KEY: str
    WEBAPP_BASE_URL: str
    MEDIA_PATH: str

def get_settings() -> Settings:
    """
    Создаёт и возвращает объект настроек.
    Если чего-то не хватает в .env — упадёт сразу.
    """
    return Settings(
        ENV=os.getenv("ENV", "development"),
        DATABASE_URL=os.environ["DATABASE_URL"],
        BOT_TOKEN=os.environ["BOT_TOKEN"],
        SECRET_KEY=os.environ["SECRET_KEY"],
        WEBAPP_BASE_URL=os.environ["WEBAPP_BASE_URL"],
        MEDIA_PATH=os.environ["MEDIA_PATH"],
    )
