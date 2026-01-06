import hmac
import hashlib
from urllib.parse import parse_qsl


def _extract_hash(payload: dict) -> str:
    """
    Telegram WebApp иногда присылает поле hash, но встречаются
    реализации, которые кладут подпись в signature. Забираем
    любой из вариантов и удаляем из словаря, чтобы не попадал
    в data_check_string.
    """
    received_hash = payload.pop("hash", None) or payload.pop("signature", None)
    if not received_hash:
        raise ValueError("Missing hash")
    return received_hash


def verify_telegram_webapp(init_data: str, bot_token: str) -> dict:
    if not init_data:
        raise ValueError("initData is empty")

    # 1. URL-DECODE
    parsed = dict(parse_qsl(init_data, strict_parsing=True))

    # 2. Забираем hash/signature
    received_hash = _extract_hash(parsed)

    # 3. Формируем data_check_string (без hash)
    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed.items())
    )

    # 4. Правильный secret_key: HMAC_SHA256("WebAppData", bot_token)
    secret_key = hmac.new(
        key=b"WebAppData",
        msg=bot_token.encode(),
        digestmod=hashlib.sha256,
    ).digest()

    # 5. Считаем hash по data_check_string
    calculated_hash = hmac.new(
        key=secret_key,
        msg=data_check_string.encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(calculated_hash, received_hash):
        raise ValueError("Invalid initData hash")

    # Возвращаем данные без hash/signature
    return parsed
