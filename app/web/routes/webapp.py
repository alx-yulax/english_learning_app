from flask import Blueprint, request, jsonify, render_template

from app.core.security import verify_telegram_webapp
from app.services.words import WordsService
from app.services.users import UsersService

webapp_bp = Blueprint("webapp", __name__)


@webapp_bp.route("/", methods=["GET"])
def webapp_index():
    """
    Entry point for Telegram WebApp
    """
    return render_template("webapp/index.html")


def get_telegram_user_from_header():
    init_data = request.headers.get("X-Telegram-InitData")
    if not init_data:
        raise ValueError("initData is required")

    data = verify_telegram_webapp(init_data)
    return data["user"]


@webapp_bp.route("/webapp/words", methods=["GET"])
def webapp_words():
    init_data = request.headers.get("X-Telegram-InitData")

    if not init_data:
        return jsonify({"error": "initData is required"}), 403

    try:
        data = verify_telegram_webapp(init_data)
        telegram_id = data["user"]["id"]
    except Exception as e:
        return jsonify({"error": str(e)}), 403

    words = WordsService.list_words_by_telegram_id(telegram_id)

    return jsonify([
        {
            "id": w.id,
            "english": w.english,
            "translation": w.translation,
        }
        for w in words
    ])
