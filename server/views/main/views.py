from flask import Blueprint, jsonify, render_template, request
from pypdf import PdfReader

from server.application import app
from server.extensions import db
from server.models.document import Document

BP = Blueprint("main", __name__, template_folder="templates")


@app.route("/upload", methods=["POST"])
def post_upload():
    if "file" not in request.files:
        return jsonify({"error": "no file uploaded"}), 400

    reader = PdfReader(request.files["file"])
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    document = Document(text=text)
    db.session.add(document)
    db.session.commit()

    return jsonify({"success": True})


@app.route("/", defaults={"path": ""}, methods=["GET"])
@app.route("/<path:path>", methods=["GET"])
def index(path):
    return render_template("main/index.jinja2")
