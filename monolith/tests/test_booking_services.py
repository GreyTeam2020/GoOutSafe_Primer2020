from random import randrange

import pytest

import datetime
from monolith.database import db, User, Restaurant, Reservation, Positive
from monolith.services import BookingServices
from monolith.tests.utils import (
    get_user_with_email,
    create_restaurants_on_db,
    create_user_on_db,
    del_restaurant_on_db,
    del_user_on_db,
    get_last_booking,
    del_friends_of_reservation,
    del_time_for_rest,
    del_booking_services,
)
from sqlalchemy import func


class Test_BookServices:
    """
    This test suite test the services about booking use case.
    All the code tested inside this class is inside the services/booking_services.py
    """

    def test_new_booking(self):
        """
        TEST FOR ADDING A RESERVATION
        test flow
        - Create a new customer
        - Create a new restaurant owner
        - create a new restaurant
        - check on Reservation (what we aspect)
        - erase friends from reservation
        - erase opening hours
        - erase restaurants (included the tables)
        - erase user
        """

        user = create_user_on_db(randrange(100000))
        rest_owner = create_user_on_db(ran=2)
        restaurant = create_restaurants_on_db(user_id=rest_owner.id)

        book = BookingServices.book(
            restaurant.id,
            user,
            datetime.datetime(year=2120, month=11, day=25, hour=13),
            4,
            "a@a.com;b@b.com;c@c.com",
        )

        book2 = BookingServices.book(
            restaurant.id,
            user,
            datetime.datetime(year=2120, month=11, day=25, hour=13),
            6,
            "a@a.com;b@b.com;c@c.com;d@d.com;e@e.com",
        )

        assert book[0] is not None
        assert book2[0] is not None

        # delete friends
        del_friends_of_reservation(book[0].id)
        del_friends_of_reservation(book2[0].id)

        # delete reservations
        del_booking_services(book[0].id)
        del_booking_services(book2[0].id)

        # delete restaurants (so also tables)
        del_restaurant_on_db(restaurant.id)

        # delete users
        del_user_on_db(user.id)
        del_user_on_db(rest_owner.id)

        # AT THE END THERE MUST TO BE ONLY ONE RESERVATION
        q = db.session.query(func.count(Reservation.id)).scalar()
        assert q == 1

    def test_new_booking_notables(self):
        """
        No more tables available
        """
        user = create_user_on_db()
        rest_owner = create_user_on_db(ran=2)
        restaurant = create_restaurants_on_db(user_id=rest_owner.id, tables=1)

        book = BookingServices.book(
            restaurant.id,
            user,
            datetime.datetime(year=2120, month=11, day=25, hour=13),
            4,
            "a@a.com;b@b.com;c@c.com",
        )

        book2 = BookingServices.book(
            restaurant.id,
            user,
            datetime.datetime(year=2120, month=11, day=25, hour=13),
            6,
            "a@a.com;b@b.com;c@c.com;d@d.com;e@e.com",
        )

        assert book[0] is not None
        assert book2[0] is None

        # delete friends
        del_friends_of_reservation(book[0].id)

        # delete reservations
        del_booking_services(book[0].id)

        # delete restaurants (so also tables)
        del_restaurant_on_db(restaurant.id)

        # delete users
        del_user_on_db(user.id)
        del_user_on_db(rest_owner.id)

        # AT THE END THERE MUST TO BE ONLY ONE RESERVATION
        q = db.session.query(func.count(Reservation.id)).scalar()
        assert q == 1

    def test_new_booking_closed(self):
        """
        restaurant closed
        """
        user = create_user_on_db()
        rest_owner = create_user_on_db(ran=2)
        restaurant = create_restaurants_on_db(user_id=rest_owner.id, tables=1)

        book = BookingServices.book(
            restaurant.id,
            user,
            datetime.datetime(year=2120, month=11, day=25, hour=10),
            4,
            "a@a.com;b@b.com;c@c.com",
        )

        assert book[0] is None

        # delete restaurants (so also tables)
        del_restaurant_on_db(restaurant.id)

        # delete users
        del_user_on_db(user.id)
        del_user_on_db(rest_owner.id)

        # AT THE END THERE MUST TO BE ONLY ONE RESERVATION
        q = db.session.query(func.count(Reservation.id)).scalar()
        assert q == 1

    def test_new_booking_overlaps(self):
        """
        overlapped reservations
        """

        user = create_user_on_db()
        rest_owner = create_user_on_db(ran=2)
        restaurant = create_restaurants_on_db(user_id=rest_owner.id, tables=1)

        book = BookingServices.book(
            restaurant.id,
            user,
            datetime.datetime(year=2120, month=11, day=25, hour=13),
            4,
            "a@a.com;b@b.com;c@c.com",
        )

        book2 = BookingServices.book(
            restaurant.id,
            user,
            datetime.datetime(year=2120, month=11, day=25, hour=13, minute=29),
            6,
            "a@a.com;b@b.com;c@c.com;d@d.com;e@e.com",
        )

        assert book[0] is not None
        assert book2[0] is None

        # delete friends
        del_friends_of_reservation(book[0].id)

        # delete reservations
        del_booking_services(book[0].id)

        # delete restaurants (so also tables)
        del_restaurant_on_db(restaurant.id)

        # delete users
        del_user_on_db(user.id)
        del_user_on_db(rest_owner.id)

        # AT THE END THERE MUST TO BE ONLY ONE RESERVATION
        q = db.session.query(func.count(Reservation.id)).scalar()
        assert q == 1

    def test_booking_in_past(self):
        """
        check if i can book in the past
        """
        """
        restaurant closed
        """
        user = create_user_on_db()
        rest_owner = create_user_on_db(ran=2)
        restaurant = create_restaurants_on_db(user_id=rest_owner.id, tables=1)

        book = BookingServices.book(
            restaurant.id,
            user,
            datetime.datetime(year=1999, month=11, day=25, hour=10),
            4,
            "a@a.com;b@b.com;c@c.com",
        )

        assert book[0] is None

        # delete restaurants (so also tables)
        del_restaurant_on_db(restaurant.id)

        # delete users
        del_user_on_db(user.id)
        del_user_on_db(rest_owner.id)

        # AT THE END THERE MUST TO BE ONLY ONE RESERVATION
        q = db.session.query(func.count(Reservation.id)).scalar()
        assert q == 1

    def test_delete_booking(self):
        """
        test for deletion
        """

        user = create_user_on_db()
        rest_owner = create_user_on_db(ran=2)
        restaurant = create_restaurants_on_db(user_id=rest_owner.id)

        book = BookingServices.book(
            restaurant.id,
            user,
            datetime.datetime(year=2120, month=11, day=25, hour=12),
            6,
            "a@a.com;b@b.com;c@c.com;d@d.com;e@e.com",
        )

        assert book[0] is not None

        # delete the reservation
        BookingServices.delete_book(book[0].id, user.id)
        # check how many reservations
        q = db.session.query(func.count(Reservation.id)).scalar()
        assert q == 1

        # delete restaurants (so also tables)
        del_restaurant_on_db(restaurant.id)

        # delete users
        del_user_on_db(user.id)
        del_user_on_db(rest_owner.id)

    def test_update_booking(self):
        """
        this test insert two reservation that should be ok
        """
        user = create_user_on_db()
        rest_owner = create_user_on_db(ran=2)
        restaurant = create_restaurants_on_db(user_id=rest_owner.id)

        book = BookingServices.book(
            restaurant.id,
            user,
            datetime.datetime(year=2120, month=11, day=25, hour=13),
            4,
            "a@a.com;b@b.com;c@c.com",
        )

        assert book[0] is not None

        book = BookingServices.update_book(
            book[0].id,
            user,
            datetime.datetime(year=2120, month=11, day=25, hour=14),
            2,
            "a@a.com",
        )
        assert book[0] is not None

        # delete friends
        del_friends_of_reservation(book[0].id)

        # delete reservations
        del_booking_services(book[0].id)

        # delete restaurants (so also tables)
        del_restaurant_on_db(restaurant.id)

        # delete users
        del_user_on_db(user.id)
        del_user_on_db(rest_owner.id)

        # AT THE END THERE MUST TO BE ONLY ONE RESERVATION
        q = db.session.query(func.count(Reservation.id)).scalar()
        assert q == 1
