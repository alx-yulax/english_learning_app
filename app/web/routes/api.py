from datetime import datetime
from app.database.session import SessionLocal
from app.database.models import User, Repetition

from flask import Blueprint, request, jsonify
from functools import wraps

from app.core.security import (
    verify_telegram_webapp,
    TelegramWebAppAuthError,
)

api_bp = Blueprint("api", __name__, url_prefix="/api")



def telegram_webapp_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        init_data = request.headers.get("X-Telegram-Init-Data")

        if not init_data:
            return jsonify({"error": "Missing initData"}), 401

        try:
            user = verify_telegram_webapp(init_data)
        except TelegramWebAppAuthError as e:
            return jsonify({"error": str(e)}), 403

        request.telegram_user = user
        return fn(*args, **kwargs)

    return wrapper


@api_bp.route("/me")
@telegram_webapp_required
def me():
    user = request.telegram_user
    return {
        "telegram_id": user["id"],
        "username": user.get("username"),
        "first_name": user.get("first_name"),
    }

@api_bp.route("/repetitions")
@telegram_webapp_required
def repetitions():
    tg_user = request.telegram_user
    telegram_id = tg_user["id"]

    with SessionLocal() as db:
        user = (
            db.query(User)
            .filter(User.telegram_id == telegram_id)
            .one_or_none()
        )

        if not user:
            return jsonify([])

        now = datetime.utcnow()

        repetitions = (
            db.query(Repetition)
            .join(Repetition.word)
            .filter(
                Repetition.next_repeat_at <= now,
                Repetition.word.has(user_id=user.id),
            )
            .order_by(Repetition.next_repeat_at)
            .limit(20)
            .all()
        )

        result = []
        for r in repetitions:
            word = r.word
            result.append({
                "repetition_id": r.id,
                "translation": word.translation,
                "image_url": word.image_path,
                "has_audio": bool(word.audio_path),
            })

        return jsonify(result)
