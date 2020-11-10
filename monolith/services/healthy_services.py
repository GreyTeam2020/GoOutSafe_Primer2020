from datetime import datetime

from monolith.database import (
    db,
    Positive,
    User,
    OpeningHours,
    RestaurantTable,
    Reservation,
    Restaurant,
)
from sqlalchemy.orm import aliased
from datetime import datetime, timedelta
from sqlalchemy import cast, Date, extract

from monolith.services import UserService
from monolith.utils import send_mail


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

        q_already_positive = (
            db.session.query(Positive)
            .filter_by(user_id=q_user.first().id, marked=True)
            .first()
        )

        if q_already_positive is None:
            new_positive = Positive()
            new_positive.from_date = datetime.today()
            new_positive.marked = True
            new_positive.user_id = q_user.first().id

            db.session.add(new_positive)
            db.session.commit()

            # send email to restaurants where there was a positive
            q_restaurants = (
                db.session.query(Restaurant)
                .filter(
                    new_positive.user_id == Reservation.customer_id,
                    Reservation.table_id == RestaurantTable.id,
                    RestaurantTable.restaurant_id == Restaurant.id,
                    Reservation.reservation_date <= datetime.today(),
                    Reservation.reservation_date
                    >= datetime.today() - timedelta(days=14),
                )
                .all()
            )

            for restaurant in q_restaurants:

                """DDEFINIRE UNA MAIL PER IL RISTORATORE e mandarla"""

            # send email to people that were in the same restauant
            # of a positive person
            reservation_positive = aliased(Reservation)
            reservations_clients = aliased(Reservation)
            Table_positive = aliased(RestaurantTable)
            Tables_clients = aliased(RestaurantTable)

            q_contacts = (
                db.session.query(reservations_clients, Restaurant)
                .filter(
                    new_positive.user_id == reservation_positive.customer_id,
                    reservation_positive.table_id == Table_positive.id,
                    Table_positive.restaurant_id == Restaurant.id,
                    Restaurant.id == Tables_clients.restaurant_id,
                    Tables_clients.id == reservations_clients.table_id,
                    OpeningHours.restaurant_id == Restaurant.id,
                    reservation_positive.reservation_date.cast(Date)
                    == reservations_clients.reservation_date.cast(Date),
                    reservation_positive.reservation_date <= datetime.today(),
                    reservation_positive.reservation_date
                    >= datetime.today() - timedelta(days=14),
                    (
                        (
                            (
                                reservation_positive.reservation_date
                                >= OpeningHours.open_dinner
                            )
                            & (
                                reservations_clients.reservation_date
                                >= OpeningHours.open_dinner
                            )
                        )
                        | (
                            (
                                reservation_positive.reservation_date
                                <= OpeningHours.close_lunch
                            )
                            & (
                                reservations_clients.reservation_date
                                <= OpeningHours.close_lunch
                            )
                        )
                    ),
                )
                .all()
            )

            for contact in q_contacts:
                users = (
                    db.session.query(User)
                    .filter(
                        User.id == contact[0].customer_id,
                        User.id == Positive.user_id,
                        Positive.marked == True,
                    )
                    .first()
                )

                # if the user is already positive i don't show him
                if users is None:
                    user = (
                        db.session.query(User)
                        .filter(User.id == contact[0].customer_id)
                        .first()
                    )
                    """
                    Send the email!

                    print(user.email, user.firstname, 
                            contact[0].reservation_date, contact[1].name)
                

                    sendPossibilePositiveContact(user.email, user.firstname, 
                        contact[0].reservation_date.cast(Date), contact[1].name)
                    """
            return ""
        else:
            return "User with email {} already Covid-19 positive".format(user_email)

    @staticmethod
    def search_contacts(id_user):
        result = []
        all_reservations = db.session.query(Reservation).filter(Reservation.reservation_date >= (datetime.today()-timedelta(days=14)), Reservation.reservation_date < datetime.today()).all()
        for reservation in all_reservations:
            table = db.session.query(RestaurantTable).filter_by(id=reservation.table_id).first()
            opening = db.session.query(OpeningHours).filter(OpeningHours.restaurant_id == table.restaurant_id, OpeningHours.week_day==reservation.reservation_date.weekday()).first()
            period = [opening.open_dinner, opening.close_dinner] if (opening.open_dinner <= reservation.reservation_date.time()) else [opening.open_lunch, opening.close_lunch]

            all_contacts = db.session.query(Reservation).filter(
                extract("day", Reservation.reservation_date) == extract("day", reservation.reservation_date),
                extract("month", Reservation.reservation_date) == extract("month", reservation.reservation_date),
                extract("year", Reservation.reservation_date) == extract("year", reservation.reservation_date),
                extract("hour", Reservation.reservation_date) >= extract("hour", period[0]),
                extract("hour", Reservation.reservation_date) <= extract("hour", period[1]),
            ).all()
            for contact in all_contacts:
                if contact.customer_id not in result:
                    result.append(contact.customer_id)
        touser = db.session.query(User).filter(User.id.in_(result)).all()
        contact_users = []

        for user in touser:
            if not UserService.is_positive(user.id):
                contact_users.append(
                    [
                        user.id,
                        user.firstname + " " + user.lastname,
                        str(user.dateofbirth).split()[0],
                        user.email,
                        user.phone,
                    ])

        return contact_users

    @staticmethod
    def unmark_positive(user_email: str, user_phone: str) -> str:
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

        q_already_positive = (
            db.session.query(Positive)
            .filter_by(user_id=q_user.first().id, marked=True)
            .first()
        )

        if q_already_positive is not None:
            q_already_positive.marked = False
            db.session.commit()
            return ""
        else:
            return "User with email {} is not Covid-19 positive".format(user_email)
