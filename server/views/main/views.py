# from itertools import batched

from itertools import islice

from flask import Blueprint, jsonify, render_template, request
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

from server.application import app
from server.extensions import db
from server.models.document import Chunk, Document

BP = Blueprint("main", __name__, template_folder="templates")


def batched(iterable, n, *, strict=False):
    # batched('ABCDEFG', 3) → ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    iterator = iter(iterable)
    while batch := tuple(islice(iterator, n)):
        if strict and len(batch) != n:
            raise ValueError("batched(): incomplete batch")
        yield batch


@app.route("/upload", methods=["POST"])
def post_upload():
    if "file" not in request.files:
        return jsonify({"error": "no file uploaded"}), 400

    reader = PdfReader(request.files["file"])
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    model = SentenceTransformer("all-MiniLM-L6-v2")
    sentences = ["".join(chars) for chars in batched(text, 1024)]
    embeddings = model.encode(sentences)

    chunks = [
        Chunk(text=text, vectors=vectors)
        for text, vectors in zip(sentences, embeddings)
    ]
    document = Document(text=text, chunks=chunks)
    db.session.add(document)
    db.session.commit()

    return jsonify({"success": True})


@app.route("/", defaults={"path": ""}, methods=["GET"])
@app.route("/<path:path>", methods=["GET"])
def index(path):
    return render_template("main/index.jinja2")
