import datetime
from sqlalchemy import or_, cast

from monolith.database import (
    db,
    RestaurantTable,
    Reservation,
    Restaurant,
    OpeningHours,
    Positive,
)


class BookingServices:

    @staticmethod
    def book(restaurant_id, current_user, py_datetime, people_number):
        # if user wants to book in the past..
        if py_datetime < datetime.datetime.now():
            return (False, "You can not book in the past!")
        # check if the user is positive
        is_positive = (
            db.session.query(Positive)
            .filter_by(user_id=current_user.id)
            .filter_by(marked=True)
            .first()
        )
        if is_positive:
            return (False, "You are marked as positive!")


        week_day = py_datetime.weekday()
        only_time = py_datetime.time()

        # check if the restaurant is open. 12 in open_lunch means open at lunch. 20 in open_dinner means open at dinner.
        opening_hour = (
            db.session.query(OpeningHours)
            .filter_by(restaurant_id=restaurant_id)
            .filter_by(week_day=week_day)
            .first()
        )

        
        # the restaurant is closed
        if opening_hour is None:
            print("No Opening hour")
            return (False, "The restaurant is closed")

        # strange situation.. but it could be happen
        # opening hour is in db but the resturant is closed both lunch and dinner
        if opening_hour.open_lunch is None and opening_hour.open_dinner is None:
            return (False, "The restaurant is closed")

        # if the resturant is open only at lunch or at dinner do some checks..
        if (opening_hour.open_lunch is None or opening_hour.close_lunch is None) and (
            only_time < opening_hour.open_dinner
            or only_time > opening_hour.close_dinner
        ):
            return (False, "The restaurant is closed")

        if (opening_hour.open_dinner is None or opening_hour.close_dinner is None) and (
            only_time < opening_hour.open_lunch or only_time > opening_hour.close_lunch
        ):
            return (False, "The restaurant is closed")
        #

        # if the resturant is opened both at dinner and lunch
        if opening_hour.open_lunch is not None and opening_hour.open_dinner is not None:
            # asked for some hours outside the opening hours
            if opening_hour.open_lunch > only_time:
                print("before lunch")
                return (False, "The restaurant is closed")

            if (
                opening_hour.open_dinner > only_time
                and opening_hour.close_lunch < only_time
            ):
                print("between")
                return (False, "The restaurant is closed")

            if opening_hour.close_dinner < only_time:
                print("after dinner")
                return (False, "The restaurant is closed")
            #

        # now let's see if there is a table
        
        '''
        get the time delta (avg_time) from the restaurant table
        '''
        avg_time = (db.session.query(Restaurant)
                    .filter_by(id = restaurant_id)
                    .first()
                    .avg_time)

        '''
        get all the reservation (with the reservation_date between the dates in which I want to book)
        or (or the reservation_end between the dates in which I want to book)
        the dates in which I want to book are:
        start = py_datetime  
        end = py_datetime + avg_time

        always filtered by the people_number  
        '''
        reservations = (
            db.session.query(RestaurantTable.id)
                .join(Reservation, RestaurantTable.id == Reservation.table_id)
                .filter(RestaurantTable.restaurant_id == restaurant_id)
                .filter(or_(
                Reservation.reservation_date.between(py_datetime, py_datetime+datetime.timedelta(minutes=avg_time)),
                Reservation.reservation_end.between(py_datetime, py_datetime+datetime.timedelta(minutes=avg_time))
                ))
                .filter(RestaurantTable.max_seats >= people_number)
        )


        # from the list of all tables in the restaurant (the ones in which max_seats < number of people requested) drop the reserved ones
        all_restaurant_tables = (
            db.session.query(RestaurantTable)
            .filter(RestaurantTable.max_seats >= people_number)
            .filter_by(restaurant_id=restaurant_id)
            .filter(~RestaurantTable.id.in_(reservations))
            .all()
        )

        # if there are tables available.. get the one with minimum max_seats
        print ("OK, Ther are {} tables available".format(len(all_restaurant_tables)))
        if len(all_restaurant_tables) > 0:
            min_value = (
                all_restaurant_tables[0].id,
                all_restaurant_tables[0].max_seats,
            )
            for i in range(1, len(all_restaurant_tables)):
                if all_restaurant_tables[i].max_seats < min_value[1]:
                    min_value = (
                        all_restaurant_tables[i].id,
                        all_restaurant_tables[i].max_seats,
                    )

            # get restaurant and table name
            restaurant_name = (
                db.session.query(Restaurant.name).filter_by(id=restaurant_id).first()[0]
            )
            table_name = (
                db.session.query(RestaurantTable.name)
                .filter_by(id=min_value[0])
                .first()[0]
            )

            # register on db the reservation
            new_reservation = Reservation()
            new_reservation.reservation_date = py_datetime
            new_reservation.customer_id = current_user.id
            new_reservation.table_id = min_value[0]
            new_reservation.people_number = people_number
            db.session.add(new_reservation)
            db.session.commit()

            return (True, restaurant_name, table_name)
        else:
            return (False, "no tables available")
