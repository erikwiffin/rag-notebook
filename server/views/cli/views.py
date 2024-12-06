import click
from flask import Blueprint

from server.application import app

BP = Blueprint("cli", __name__)


@app.cli.command()
def hello():
    click.echo("Hello World!")
