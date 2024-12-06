import os

from celery import Celery, Task
from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

# SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Elasticsearch
# app.config['ELASTICSEARCH_DATABASE_URI'] = os.getenv('ELASTICSEARCH_DATABASE_URI')

# Flask Vite
app.config["VITE_AUTO_INSERT"] = False

# Celery
app.config.from_mapping(
    CELERY=dict(
        broker_url=os.getenv("CELERY_BROKER_URL"),
        result_backend=os.getenv("CELERY_RESULT_BACKEND"),
        task_ignore_result=True,
        broker_connection_retry_on_startup=True,
    ),
)


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


def create_app():
    from server import extensions

    # from server.lib import filters
    from server.views.cli.views import BP as cli_blueprint
    from server.views.graphql.views import BP as graphql_blueprint
    from server.views.main.views import BP as main_blueprint

    app.register_blueprint(cli_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(graphql_blueprint)

    extensions.alembic.init_app(app)
    extensions.db.init_app(app)
    # extensions.es.init_app(app)
    extensions.vite.init_app(app)
    celery_init_app(app)

    return app
