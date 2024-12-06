from flask import Blueprint, render_template

from server.application import app

BP = Blueprint("main", __name__, template_folder="templates")


@app.route("/", defaults={"path": ""}, methods=["GET"])
@app.route("/<path:path>", methods=["GET"])
def index(path):
    return render_template("main/index.jinja2")
