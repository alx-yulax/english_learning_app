from flask import Blueprint, request, jsonify, render_template
from app.core.security import verify_telegram_webapp

webapp_bp = Blueprint("webapp", __name__)


@webapp_bp.route("/", methods=["GET"])
def webapp_index():
    return render_template("webapp/index.html")


@webapp_bp.route("/api/webapp/auth", methods=["POST"])
def webapp_auth():
    payload = request.json or {}
    init_data = payload.get("initData")

    if not init_data:
        return jsonify({"error": "initData is required"}), 400

    try:
        data = verify_telegram_webapp(init_data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 403

    return jsonify(
        status="ok",
        user=data["user"],
    )
