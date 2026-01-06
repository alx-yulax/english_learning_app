from flask import Blueprint, request, jsonify

from app.core.config import get_settings
from app.core.security import verify_telegram_webapp
from app.services.words import WordsService

settings = get_settings()

words_bp = Blueprint("words", __name__, url_prefix="/webapp")


@words_bp.route("/words", methods=["GET"])
def get_words():
    """
    Возвращает список слов текущего пользователя.
    Пользователь определяется ТОЛЬКО через Telegram initData.
    """
    init_data = request.headers.get("X-Telegram-InitData")
    if not init_data:
        return jsonify({"error": "Missing initData"}), 401

    try:
        data = verify_telegram_webapp(init_data, bot_token=settings.BOT_TOKEN)
    except ValueError as e:
        return jsonify({"error": str(e)}), 403

    user = data.get("user")
    if not user:
        return jsonify({"error": "No user in initData"}), 403

    telegram_id = user["id"]

    words = WordsService.list_words_by_telegram_id(telegram_id)

    return jsonify(
        [
            {
                "id": w.id,
                "translation": w.translation,
                "image_url": w.image_url,
                # ⚠️ английское слово намеренно НЕ отдаём
            }
            for w in words
        ]
    )
