from flask import Blueprint, request, jsonify, render_template

from app.bot.handlers.start import settings
from app.core.security import verify_telegram_webapp

webapp_bp = Blueprint("webapp", __name__)

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