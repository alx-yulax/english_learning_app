from flask import Blueprint, render_template

webapp_bp = Blueprint(
    "webapp",
    __name__,
    url_prefix="/webapp"
)


@webapp_bp.route("/")
def index():
    return render_template("webapp.html")
