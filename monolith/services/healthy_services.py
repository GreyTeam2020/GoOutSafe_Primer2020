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
        else:
            return "User with email {} already Covid-19 positive".format(user_email)



    @staticmethod
    def search_contacts(id_user):
        """
        This method search for people that where in the same restaurant 
        of a positive
        :return: return the list of contacts
        """
        

        #searching for the contacts
        reservation_positive = aliased(Reservation)
        reservations_clients = aliased(Reservation)
        Table_positive = aliased(RestaurantTable)
        Tables_clients = aliased(RestaurantTable)

        q_contacts = db.session.query(User).filter(
                id_user==reservation_positive.customer_id, 
                reservation_positive.table_id == Table_positive.id,
                Table_positive.restaurant_id==Restaurant.id,
                Restaurant.id == Tables_clients.restaurant_id,
                Tables_clients.id == reservations_clients.table_id,
                OpeningHours.restaurant_id == Restaurant.id,

                reservation_positive.reservation_date.cast(Date) == reservations_clients.reservation_date.cast(Date),
                reservation_positive.reservation_date <= datetime.today(),
                reservation_positive.reservation_date >= datetime.today() -timedelta(days=14),
                ( 
                    (
                        (reservation_positive.reservation_date >= OpeningHours.open_dinner) &
                        (reservations_clients.reservation_date >= OpeningHours.open_dinner)
                    ) |
                    (
                        (reservation_positive.reservation_date <= OpeningHours.close_lunch) &
                        (reservations_clients.reservation_date <= OpeningHours.close_lunch)
                    )
                ),
                User.id==id_user
            )
       
        return q_contacts
