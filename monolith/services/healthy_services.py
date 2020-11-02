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
            .filter(Positive.user_id == q_user.first().id, Positive.marked == True)
            .first()
        )

        if q_already_positive is None:
            new_positive = Positive()
            new_positive.from_date = datetime.today()
            new_positive.marked = True
            new_positive.user_id = q_user.first().id

            db.session.add(new_positive)
            db.session.commit()

            # start notification zone
            
            #to notify restaurants with a booking of the positive customer
            restaurant_notified = []
            all_reservations = (
                db.session.query(Reservation)
                .filter(
                    Reservation.reservation_date >= datetime.today(),
                    Reservation.customer_id == new_positive.user_id
                )
                .all()
            )
            for reservation in all_reservations:
                restaurant = (
                    db.session.query(Restaurant)
                    .filter(
                        reservation.table_id == RestaurantTable.id,
                        RestaurantTable.restaurant_id == Restaurant.id
                    ).first()
                )

                

                if restaurant.id not in restaurant_notified:
                    restaurant_notified.append(restaurant.id)

                    q_owner= db.session.query(User).filter(
                        User.id == restaurant.owner_id
                    ).first()
                    
                    '''
                    Send the email!

                    send_positive_booking_in_restaurant(q_owner.email, q_owner.firstname, q_user.first().email, restaurant.name)
                    '''


            #to notify contacts with a positive customer to restaurants and customers
            restaurant_notified = []
            user_notified = []
            all_reservations = (
                db.session.query(Reservation)
                .filter(
                    Reservation.reservation_date
                    >= (datetime.today() - timedelta(days=14)),
                    Reservation.reservation_date < datetime.today(),
                )
                .all()
            )
            for reservation in all_reservations:
                table = (
                    db.session.query(RestaurantTable)
                    .filter_by(id=reservation.table_id)
                    .first()
                )
                opening = (
                    db.session.query(OpeningHours)
                    .filter(
                        OpeningHours.restaurant_id == table.restaurant_id,
                        OpeningHours.week_day == reservation.reservation_date.weekday(),
                    )
                    .first()
                )
                period = (
                    [opening.open_dinner, opening.close_dinner]
                    if (opening.open_dinner <= reservation.reservation_date.time())
                    else [opening.open_lunch, opening.close_lunch]
                )
                restaurant = (
                    db.session.query(Restaurant)
                    .filter_by(id=table.restaurant_id)
                    .first()
                )

                # Notify Restaurant for a positive that where inside
                if restaurant.id not in restaurant_notified:
                    restaurant_notified.append(restaurant.id)
                    owner = db.session.query(User).filter_by(id=restaurant.owner_id)
                    """
                    Send the email!

                    sendPossibilePositiveContact(owner.email, owner.firstname, reservation.reservation_date, restaurant.name)
                    """

                all_contacts = (
                    db.session.query(Reservation)
                    .filter(
                        extract("day", Reservation.reservation_date)
                        == extract("day", reservation.reservation_date),
                        extract("month", Reservation.reservation_date)
                        == extract("month", reservation.reservation_date),
                        extract("year", Reservation.reservation_date)
                        == extract("year", reservation.reservation_date),
                        extract("hour", Reservation.reservation_date)
                        >= extract("hour", period[0]),
                        extract("hour", Reservation.reservation_date)
                        <= extract("hour", period[1]),
                    )
                    .all()
                )
                for contact in all_contacts:
                    if contact.customer_id not in user_notified:
                        user_notified.append(contact.customer_id)
                        thisuser = (
                            db.session.query(User)
                            .filter_by(id=contact.customer_id)
                            .first()
                        )
                        if thisuser is not None:
                            """
                            Send the email!

                            sendPossibilePositiveContact(thisuser.email, thisuser.firstname, contact.reservation_date, restaurant.name)
                            """
            return ""
        else:
            return "User with email {} already Covid-19 positive".format(user_email)


    @staticmethod
    def search_contacts(id_user):
        result = []
        all_reservations = (
            db.session.query(Reservation)
            .filter(
                Reservation.reservation_date >= (datetime.today() - timedelta(days=14)),
                Reservation.reservation_date < datetime.today(),
                Reservation.customer_id == id_user
            )
            .all()
        )
        for reservation in all_reservations:
            table = (
                db.session.query(RestaurantTable)
                .filter_by(id=reservation.table_id)
                .first()
            )
            opening = (
                db.session.query(OpeningHours)
                .filter(
                    OpeningHours.restaurant_id == table.restaurant_id,
                    OpeningHours.week_day == reservation.reservation_date.weekday(),
                )
                .first()
            )
            period = (
                [opening.open_dinner, opening.close_dinner]
                if (opening.open_dinner <= reservation.reservation_date.time())
                else [opening.open_lunch, opening.close_lunch]
            )

            all_contacts = (
                db.session.query(Reservation)
                .filter(
                    extract("day", Reservation.reservation_date)
                    == extract("day", reservation.reservation_date),
                    extract("month", Reservation.reservation_date)
                    == extract("month", reservation.reservation_date),
                    extract("year", Reservation.reservation_date)
                    == extract("year", reservation.reservation_date),
                    extract("hour", Reservation.reservation_date)
                    >= extract("hour", period[0]),
                    extract("hour", Reservation.reservation_date)
                    <= extract("hour", period[1]),
                )
                .all()
            )
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
                    ]
                )

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
