from flask import Flask, jsonify

from app.core.config import get_settings
from app.web.routes.webapp import webapp_bp
from app.web.routes.words import words_bp

def create_app() -> Flask:
    settings = get_settings()

    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.SECRET_KEY

    app.register_blueprint(webapp_bp)
    app.register_blueprint(words_bp)

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify(
            status="ok",
            env=settings.ENV,
        )

    return app
