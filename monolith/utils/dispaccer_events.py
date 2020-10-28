from monolith.background import send_email_to_confirm_registration
from monolith.app_constant import *

_CELERY = False


class DispatcherMessage:
    """
    This class using a mediator patter to decide if the status of app admit
    the celery message.
    The celery message are available for the moment only in release and in some debug cases
    otherwise it is disabled.

    For instance, for the testing it is disabled.

    @author Vincenzo Palazzo v.palazzo1@studenti.unipi.it
    """

    @staticmethod
    def send_message(type_message: str, params):
        """
        This static method take and string that usually is defined inside the
        file app_constant.py and check if there is condition to dispatc the test
        :return: nothings
        """
        if type_message is REGISTRATION_EMAIL:
            if _CELERY is True:
                send_email_to_confirm_registration.apply_async(args=params)
