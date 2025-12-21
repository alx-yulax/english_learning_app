from flask import Flask
from app.core.config import settings
from app.web.routes.api import api_bp
from app.web.routes.webapp import webapp_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.SECRET_KEY

    app.register_blueprint(api_bp)
    app.register_blueprint(webapp_bp)

    return app


app = create_app()

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)