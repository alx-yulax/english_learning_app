import hmac
import hashlib
from urllib.parse import parse_qsl


def verify_telegram_webapp(init_data: str, bot_token: str) -> dict:
    if not init_data:
        raise ValueError("initData is empty")

    # 1. URL-DECODE
    parsed = dict(parse_qsl(init_data, strict_parsing=True))

    # 2. Забираем hash
    received_hash = parsed.pop("hash", None)
    if not received_hash:
        raise ValueError("Missing hash")

    # 3. Формируем data_check_string
    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed.items())
    )

    # 4. 🔥 ПРАВИЛЬНЫЙ secret_key
    secret_key = hmac.new(
        key=bot_token.encode(),
        msg=b"WebAppData",
        digestmod=hashlib.sha256,
    ).digest()

    # 5. Считаем hash
    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256,
    ).hexdigest()

    # DEBUG — сейчас оставь
    print("DATA CHECK STRING:\n", data_check_string)
    print("CALC:", calculated_hash)
    print("RECV:", received_hash)

    if not hmac.compare_digest(calculated_hash, received_hash):
        raise ValueError("Invalid initData hash")

    return parsed
