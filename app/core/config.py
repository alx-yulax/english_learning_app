from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")


class Settings:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    WEBAPP_SECRET: str = os.getenv("WEBAPP_SECRET")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    MEDIA_PATH: Path = BASE_DIR / "media"


settings = Settings()
