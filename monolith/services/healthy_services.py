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
from sqlalchemy import cast, Date
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
            .filter(Positive.user_id==q_user.first().id, Positive.marked==True)
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
                db.session.query(Restaurant, Reservation)
                .filter(
                    new_positive.user_id == Reservation.customer_id,
                    Reservation.table_id == RestaurantTable.id,
                    RestaurantTable.restaurant_id == Restaurant.id,
                    Reservation.reservation_date <= datetime.today(),
                    Reservation.reservation_date >= datetime.today() - timedelta(days=14),
                )
                .all()
            )

            for restaurant in q_restaurants:

                q_owner = db.session.query(User).filter(
                    restaurant[0].owner_id == User.id,
                ).first()

                """
                print(
                    q_owner.email, q_owner.firstname, 
                    restaurant[1].reservation_date, restaurant[0].name
                )
                MAIL AI RISTORANTI
                send_positive_in_restaurant(
                    q_owner.email, q_owner.name, 
                    restaurant[1].reservation_date, restaurant[0].name
                )
                """


            # send email to people that were in the same restaurant
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
                    
                    """MANDARE LA MAIL AI CONTATTI
                    sendPossibilePositiveContact(user.email, user.firstname, 
                        contact[0].reservation_date.cast(Date), contact[1].name)
                    """
                
            return ""
        else:
            return "User with email {} already Covid-19 positive".format(user_email)

    @staticmethod
    def search_contacts(id_user):
        """
        This method search for people that where in the same restaurant
        of a positive
        :return: return the list of contacts
        """

        # searching for the contacts
        reservation_positive = aliased(Reservation)
        reservations_clients = aliased(Reservation)
        Table_positive = aliased(RestaurantTable)
        Tables_clients = aliased(RestaurantTable)

        q_contacts = (
            db.session.query(reservations_clients)
            .filter(
                id_user == reservation_positive.customer_id,
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
            .distinct()
            .all()
        )

        contact_users = []

        i = 1
        for contact in q_contacts:
            users = (
                db.session.query(User, Positive)
                .filter(
                    User.id == contact.customer_id,
                    User.id == Positive.user_id,
                    Positive.marked == True,
                )
                .first()
            )

            # if the user is already positive i don't show him
            if users is None:
                user = (
                    db.session.query(User)
                    .filter(User.id == contact.customer_id)
                    .first()
                )

                contact_users.append(
                    [
                        i,
                        user.firstname + " " + user.lastname,
                        str(user.dateofbirth).split()[0],
                        user.email,
                        user.phone,
                    ]
                )
                i += 1

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
        