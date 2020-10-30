import os

import pytest

import datetime
from monolith.database import db, User, Restaurant, Reservation
from monolith.services import BookingServices


@pytest.mark.usefixtures("client")
class Test_UserServices:
    def test_new_booking(self):
        """
        this test insert two reservation that should be ok
        """
        user = db.session.query(User).filter_by(email="john.doe@email.com").first()
        restaurant = (
            db.session.query(Restaurant).filter_by(name="Trial Restaurant").first()
        )

        d1 = datetime.datetime(year=2020, month=11, day=23, hour=12)
        book1 = BookingServices.book(restaurant.id, user, d1, 4)
        book2 = BookingServices.book(restaurant.id, user, d1, 6)

        assert book1[0] == True
        assert book2[0] == True

        db.session.query(Reservation).filter_by(reservation_date=d1).delete()
        db.session.commit()

    def test_new_booking_2(self):
        """
        this test insert two reservation and in the second one,
        there should not be another table capable of 6 people
        """
        user = db.session.query(User).filter(User.email == "john.doe@email.com").first()
        restaurant = (
            db.session.query(Restaurant).filter_by(name="Trial Restaurant").first()
        )
        d1 = datetime.datetime(year=2020, month=11, day=23, hour=12)

        book1 = BookingServices.book(restaurant.id, user, d1, 6)
        book2 = BookingServices.book(restaurant.id, user, d1, 6)

        assert book1[0] == True
        assert book2[0] == False

        db.session.query(Reservation).filter_by(reservation_date=d1).delete()
        db.session.commit()

    def test_new_booking_3(self):
        """
        restaurant closed
        """
        user = db.session.query(User).filter_by(email="john.doe@email.com").first()
        restaurant = (
            db.session.query(Restaurant).filter_by(name="Trial Restaurant").first()
        )

        d1 = datetime.datetime(year=2020, month=11, day=23, hour=10)

        book1 = BookingServices.book(restaurant.id, user, d1, 6)

        assert book1[0] == False

        db.session.query(Reservation).filter_by(reservation_date=d1).delete()
        db.session.commit()
