from celery import Celery

from monolith.app import create_worker_app
from monolith.background import calculate_rating_for_all_celery

BACKEND = "redis://{}:6379".format("rd01")
BROKER = "redis://{}:6379/0".format("rd01")


def make_celery(app):
    celery = Celery(app.import_name, backend=BACKEND, broker=BROKER)
    # celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


flask_app = create_worker_app()
celery = make_celery(flask_app)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    This task make a calculation of review rating inside each
    this task take the db code and call the RestaurantServices for each restaurants
    """
    # Calls RestaurantServices.calculate_rating_for_all() every 30 seconds
    sender.add_periodic_task(30.0, calculate_rating_for_all_celery, name="Rating")
