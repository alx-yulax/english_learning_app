from flask import Blueprint, request, jsonify

from app.core.security import verify_telegram_webapp

webapp_bp = Blueprint("webapp", __name__)


@webapp_bp.route("/webapp/auth", methods=["POST"])
def webapp_auth():
    payload = request.json or {}
    init_data = payload.get("initData")

    try:
        data = verify_telegram_webapp(init_data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 403

    return jsonify(
        status="ok",
        user=data.get("user"),
    )
