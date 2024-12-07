from pathlib import Path

import click
from flask import Blueprint
from sqlalchemy import text

from server.application import app
from server.extensions import db
from server.lib.document_service import make_document_from_pdf

BP = Blueprint("cli", __name__)


@app.cli.command()
def reset():
    db.session.execute(text("TRUNCATE TABLE document RESTART IDENTITY CASCADE"))
    db.session.commit()

    path = Path(app.instance_path) / "sample-texts"
    files = path.glob("*.pdf")

    for file in files:
        click.echo(f"Importing {file.name}")
        document = make_document_from_pdf(file)
        db.session.add(document)

    db.session.commit()
