from flask import Flask, jsonify

from app.core.config import get_settings


def create_app() -> Flask:
    settings = get_settings()

    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.SECRET_KEY

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify(
            status="ok",
            env=settings.ENV,
        )

    return app
