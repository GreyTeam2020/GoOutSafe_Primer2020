from celery import Celery
from monolith.utils import send_registration_confirm

## redis inside the http is the name of network that is called like the containser
## a good reference is https://stackoverflow.com/a/55410571/7290562
BACKEND = "redis://0.0.0.0:6379"
BROKER = "redis://0.0.0.0:6379/0"
celery = Celery(__name__, backend=BACKEND, broker=BROKER)


@celery.task()
def send_email_to_confirm_registration(to_email: str, to_name: str, with_toke: str):
    """
    Perform the celery task to send the email registration
    it take the following element
    :param to_email: Email to send the message
    :param to_name: The user name to send the message
    :param with_toke: The token of user on system
    """
    send_registration_confirm(to_email, to_name, with_toke)
