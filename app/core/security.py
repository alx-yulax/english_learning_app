import hmac
import hashlib
import time
from urllib.parse import parse_qsl

from app.core.config import get_settings


def verify_telegram_webapp(init_data: str) -> dict:
    """
    Проверяет initData от Telegram Web App.
    Возвращает payload (dict) или кидает ValueError.
    """
    if not init_data:
        raise ValueError("Empty initData")

    settings = get_settings()

    data = dict(parse_qsl(init_data, strict_parsing=True))
    received_hash = data.pop("hash", None)

    if not received_hash:
        raise ValueError("Missing hash")

    # Проверка auth_date (не старше 1 дня)
    auth_date = int(data.get("auth_date", 0))
    if time.time() - auth_date > 86400:
        raise ValueError("initData expired")

    # Формируем data_check_string
    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(data.items())
    )

    secret_key = hashlib.sha256(settings.BOT_TOKEN.encode()).digest()
    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(calculated_hash, received_hash):
        raise ValueError("Invalid initData hash")

    return data
