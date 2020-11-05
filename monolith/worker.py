from celery import Celery
from celery.schedules import crontab

from monolith.app import create_worker_app
from monolith.background import *

# Thanks to https://github.com/nebularazer/flask-celery-example
# for explaining how to implement Celery

def create_celery(app):

    BACKEND = "redis://{}:6379".format("rd01")
    BROKER = "redis://{}:6379/0".format("rd01")
    celery = Celery(__name__, backend=BACKEND, broker=BROKER)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


app = create_worker_app()
celery = create_celery(app)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(30.0, calculate_rating_on_background.s(), name=f"rating_task")