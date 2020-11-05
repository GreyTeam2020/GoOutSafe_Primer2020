from celery import Celery
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
celery = Celery()


def register_extensions(app, worker=False):
    db.init_app(app)
    global celery

    # load celery config
    BACKEND = "redis://{}:6379".format("rd01")
    BROKER = "redis://{}:6379/0".format("rd01")
    celery = Celery(__name__, backend=BACKEND, broker=BROKER)

    if not worker:
        # register celery irrelevant extensions
        pass