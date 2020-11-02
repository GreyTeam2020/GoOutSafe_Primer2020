import pytest

import datetime
from monolith.database import db, User, Restaurant, Reservation, Positive
from monolith.services import BookingServices


@pytest.mark.usefixtures("client")
class Test_BookServices:
    def test_new_booking(self):
        """
        this test insert two reservation that should be ok
        """
        user = db.session.query(User).filter_by(email="john.doe@email.com").first()
        restaurant = (
            db.session.query(Restaurant).filter_by(name="Trial Restaurant").first()
        )

        d1 = datetime.datetime(year=2120, month=11, day=25, hour=12)
        book1 = BookingServices.book(restaurant.id, user, d1, 4)
        book2 = BookingServices.book(restaurant.id, user, d1, 6)

        assert book1[0] is True
        assert book2[0] is True

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
        d1 = datetime.datetime(year=2120, month=11, day=25, hour=12)

        book1 = BookingServices.book(restaurant.id, user, d1, 6)
        book2 = BookingServices.book(restaurant.id, user, d1, 6)

        assert book1[0] is True
        assert book2[0] is False

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

        d1 = datetime.datetime(year=2120, month=11, day=25, hour=10)

        book1 = BookingServices.book(restaurant.id, user, d1, 6)

        assert book1[0] is False

        db.session.query(Reservation).filter_by(reservation_date=d1).delete()
        db.session.commit()

    def test_new_booking_4(self):
        """
        overlapped reservations
        """
        user = db.session.query(User).filter_by(email="john.doe@email.com").first()
        restaurant = (
            db.session.query(Restaurant).filter_by(name="Trial Restaurant").first()
        )

        d1 = datetime.datetime(year=2120, month=11, day=25, hour=12)
        d2 = datetime.datetime(year=2120, month=11, day=25, hour=12, minute=29)

        book1 = BookingServices.book(restaurant.id, user, d1, 2)
        book2 = BookingServices.book(restaurant.id, user, d1, 2)
        book3 = BookingServices.book(restaurant.id, user, d2, 2)

        assert book1[0] == True
        assert book2[0] == True
        assert book3[0] == False

        db.session.query(Reservation).filter_by(reservation_date=d1).delete()
        db.session.query(Reservation).filter_by(reservation_date=d2).delete()
        db.session.commit()

    def test_booking_positive(self):
        """
        mark user as positive
        check if i can book
        """
        user = db.session.query(User).filter_by(email="john.doe@email.com").first()
        assert user is not None

        new_positive = Positive()
        new_positive.from_date = datetime.datetime.today()
        new_positive.marked = True
        new_positive.user_id = user.id

        db.session.add(new_positive)
        db.session.commit()

        restaurant = (
            db.session.query(Restaurant).filter_by(name="Trial Restaurant").first()
        )
        d1 = datetime.datetime(year=2120, month=11, day=25, hour=10)
        book = BookingServices.book(restaurant.id, user, d1, 6)
        assert book[0] is False

        db.session.query(Positive).filter_by(user_id=user.id).delete()
        db.session.commit()

    def test_booking_in_past(self):
        """
        check if i can book in the past
        """
        user = db.session.query(User).filter_by(email="john.doe@email.com").first()
        assert user is not None

        restaurant = (
            db.session.query(Restaurant).filter_by(name="Trial Restaurant").first()
        )
        d1 = datetime.datetime(year=1998, month=11, day=23, hour=10)
        book = BookingServices.book(restaurant.id, user, d1, 6)
        assert book[0] is False

    def test_booking_when_closed(self):
        """
        check if i can book when restaurant is closed
        """
        user = db.session.query(User).filter_by(email="john.doe@email.com").first()
        assert user is not None

        restaurant = (
            db.session.query(Restaurant).filter_by(name="Trial Restaurant").first()
        )
        d1 = datetime.datetime(year=2120, month=11, day=26, hour=10)
        book = BookingServices.book(restaurant.id, user, d1, 6)
        assert book[0] is False

    def test_delete_booking(self):
        """
        test delete reservation by customer
        """
        user = db.session.query(User).filter_by(email="john.doe@email.com").first()
        reservation = db.session.query(Reservation).first()
        assert reservation is not None
        BookingServices.delete_book(reservation.id, user.id)
        reservation_not_present = db.session.query(Reservation).filter_by(id=reservation.id).first()
        assert reservation_not_present is None

    def test_update_booking(self):
        """
        this test insert two reservation that should be ok
        """
        user = db.session.query(User).filter_by(email="john.doe@email.com").first()
        reservation = db.session.query(Reservation).first()

        d1 = datetime.datetime(year=2120, month=11, day=25, hour=12)
        book = BookingServices.update_book(reservation.id, user, d1, 1)
        assert book[0] is True

        db.session.query(Reservation).filter_by(reservation_date=d1).delete()
        db.session.commit()
