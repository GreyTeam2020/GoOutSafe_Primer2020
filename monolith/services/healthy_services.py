from monolith.database import db


class HealthyServices:
    """
    This class is an service that have inside it all the component
    to make all operation with db about healthy authority
    """

    @staticmethod
    def mark_positive(user_email: str, user_phone: str):
        """
        This method mark the a people as positive on db
        :param user_email:
        :param user_phone:
        :return: return a message
        """
        pass
