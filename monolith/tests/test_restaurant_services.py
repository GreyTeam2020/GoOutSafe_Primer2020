import os

import pytest
from monolith.database import db, User, Restaurant, Reservation
from monolith.forms import RestaurantForm
from monolith.services.restaurant_services import RestaurantServices
from datetime import datetime

from monolith.tests.utils import get_user_with_email


@pytest.mark.usefixtures("client")
class Test_RestaurantServices:
    """
    This test suit coverage all test over Restaurant service
    @author Vincenzo Palazzo v.palazzo1@studenti.it
    """

    def test_create_restaurant(self):
        """
        test create user
        :return:
        """
        form = RestaurantForm()
        form.name = "Gino Sorbillo"
        form.phone = "096321343"
        form.lat = 12
        form.lon = 12
        form.n_tables.data = 50
        form.covid_measures.data = "We can survive"
        form.cuisine.data = ["Italian food"]
        form.open_days.data = ["0"]
        form.open_lunch.data = datetime.time(datetime(2020, 7, 1, 12, 00))
        form.close_lunch.data = datetime.time(datetime(2020, 7, 1, 12, 00))
        form.open_dinner.data = datetime.time(datetime(2020, 7, 1, 18, 00))
        form.close_dinner.data = datetime.time(datetime(2020, 6, 1, 22, 00))
        q_user = db.session.query(User).filter_by(email="ham.burger@email.com").first()
        assert q_user is not None
        restaurant = RestaurantServices.create_new_restaurant(form, q_user.id, 6)
        assert restaurant is not None

        db.session.query(Restaurant).filter_by(id=restaurant.id).delete()
        db.session.commit()

    def test_all_restaurant(self):
        """
        test about the services restaurant to test the result of all restaurants
        :return:
        """
        all_restauirants = RestaurantServices.get_all_restaurants()
        assert len(all_restauirants) == 1

    def test_reservation_local_ko_by_email(self):
        """
        This test cases, tru to test the logic inside the services to avoid
        stupid result

        http://localhost:5000/my_reservations?fromDate=2013-10-07&toDate=2014-10-07&email=john.doe@email.com
        :return:
        """
        email = "ham.burger@email.com"
        user = get_user_with_email(email)
        from_date = "2013-10-07"
        to_date = "2014-10-07"
        assert user is not None

        def_rest = db.session.query(Restaurant).all()[0]
        assert def_rest is not None
        all_reservation = RestaurantServices.get_reservation_rest(
            def_rest.owner_id, def_rest.id, from_date, to_date, email
        )
        assert len(all_reservation) == 0

    def test_reservation_local_ok_by_email(self):
        """
        This test cases, tru to test the logic inside the services to avoid
        stupid result

        http://localhost:5000/my_reservations?fromDate=2013-10-07&toDate=2014-10-07&email=john.doe@email.com
        :return:
        """
        email = "john.doe@email.com"
        user = get_user_with_email(email)
        assert user is not None
        from_date = datetime(2020, 9, 28, hour=12).isoformat()
        to_date = datetime(2020, 11, 28, hour=12).isoformat()

        def_rest = db.session.query(Restaurant).all()[0]
        assert def_rest is not None
        all_reservation = RestaurantServices.get_reservation_rest(
            def_rest.owner_id, def_rest.id, from_date, to_date, email
        )
        assert len(all_reservation) == 1
