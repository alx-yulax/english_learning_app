from flask import Blueprint, request, jsonify, render_template

from app.core.config import get_settings
from app.core.security import verify_telegram_webapp

settings = get_settings()

webapp_bp = Blueprint("webapp", __name__, url_prefix="/webapp")


@webapp_bp.route("/", methods=["GET"])
def webapp_index():
    return render_template("index.html")


@webapp_bp.route("/auth", methods=["POST"])
def webapp_auth():
    init_data = request.headers.get("X-Telegram-InitData")

    if not init_data:
        return jsonify({"error": "initData missing"}), 400

    try:
        data = verify_telegram_webapp(
            init_data=init_data,
            bot_token=settings.BOT_TOKEN,
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 403

    return jsonify(
        status="ok",
        user=data.get("user"),
    )