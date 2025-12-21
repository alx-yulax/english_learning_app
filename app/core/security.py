import hmac
import hashlib
import time
from urllib.parse import parse_qsl

from app.core.config import settings


class TelegramWebAppAuthError(Exception):
    pass


def verify_telegram_webapp(init_data: str, max_age: int = 86400) -> dict:
    """
    Проверяет подпись Telegram Web App.
    Возвращает user dict, если всё ок.
    """
    parsed = dict(parse_qsl(init_data, keep_blank_values=True))

    if "hash" not in parsed:
        raise TelegramWebAppAuthError("Missing hash")

    received_hash = parsed.pop("hash")

    # Проверка времени
    auth_date = int(parsed.get("auth_date", 0))
    if time.time() - auth_date > max_age:
        raise TelegramWebAppAuthError("Auth data expired")

    # Строка проверки
    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed.items())
    )

    # Секретный ключ
    secret_key = hmac.new(
        key=b"WebAppData",
        msg=settings.BOT_TOKEN.encode(),
        digestmod=hashlib.sha256,
    ).digest()

    calculated_hash = hmac.new(
        key=secret_key,
        msg=data_check_string.encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(calculated_hash, received_hash):
        raise TelegramWebAppAuthError("Invalid hash")

    # user приходит JSON-строкой
    if "user" not in parsed:
        raise TelegramWebAppAuthError("Missing user data")

    import json
    user = json.loads(parsed["user"])

    return user
