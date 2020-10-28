from celery import Celery
from monolith.utils import send_registration_confirm

BACKEND = BROKER = "redis://localhost:6379"
celery = Celery("gooutsafe_mb", backend=BACKEND, broker=BROKER)

_APP = None


@celery.task()
def send_email_to_confirm_registration(to_email: str, to_name: str, with_toke: str):
    """
    Perform the celery task to send the email registration
    it take the following element
    :param to_email: Email to send the message
    :param to_name: The user name to send the message
    :param with_toke: The token of user on system
    """
    send_email_to_confirm_registration(to_email, to_name, with_toke)
