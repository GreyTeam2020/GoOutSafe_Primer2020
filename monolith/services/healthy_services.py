from datetime import datetime

from monolith.database import db, Positive, User


class HealthyServices:
    """
    This class is an service that have inside it all the component
    to make all operation with db about healthy authority
    """

    @staticmethod
    def mark_positive(user_email: str, user_phone: str) -> str:
        """
        This method mark the a people as positive on db
        :param user_email:
        :param user_phone:
        :return: return a message
        """
        if user_email == "" and user_phone == "":
            return "Insert an email or a phone number"

        if user_email != "":
            q_user = db.session.query(User).filter_by(
                email=user_email,
            )
        else:
            q_user = db.session.query(User).filter_by(
                phone=user_phone,
            )

        if q_user.first() is None:
            return "The user is not registered"

        q_already_positive = db.session.query(Positive)\
            .filter_by(user_id=q_user.first().id, marked=True)\
            .first()

        if q_already_positive is None:
            new_positive = Positive()
            new_positive.from_date = datetime.today()
            new_positive.marked = True
            new_positive.user_id = q_user.first().id

            db.session.add(new_positive)
            db.session.commit()
        else:
            return "User with email {} already Covid-19 positive".format(user_email)
