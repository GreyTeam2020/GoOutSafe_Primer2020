import pytest
from monolith.database import db, User, Restaurant, Review, MenuDish, Reservation
from monolith.forms import RestaurantForm
from monolith.services.restaurant_services import RestaurantServices
from datetime import datetime

from monolith.tests.utils import (
    get_user_with_email,
    create_restaurants_on_db,
    del_restaurant_on_db,
    del_user_on_db,
    create_user_on_db,
    login,
    create_random_booking,
)


class Test_RestaurantServices:
    """
    This test suite test the services about restaurant use case.
    All the code tested inside this class is inside the services/test_restaurant_services.py
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

        del_restaurant_on_db(restaurant.id)

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
        owner = create_user_on_db(12345543234)
        assert owner is not None

        rest = create_restaurants_on_db(user_id=owner.id)
        assert rest is not None

        user = create_user_on_db(123455432332)
        assert user is not None

        date_time = datetime(2020, 10, 28, 21, 30)

        books = create_random_booking(1, rest.id, user, date_time, "a@a.com")
        assert len(books) == 1

        from_date = "2020-09-28"
        to_date = "2020-11-28"

        reservations = RestaurantServices.get_reservation_rest(
            rest.owner_id, rest.id, from_date, to_date, user.email
        )
        assert len(reservations) == 1

        del_user_on_db(user.id)
        del_restaurant_on_db(rest.id)

    def test_new_review(self):
        """
        test for the new review function
        """
        restaurant = (
            db.session.query(Restaurant.id)
            .filter(Restaurant.name == "Trial Restaurant")
            .first()
        )
        reviewer = (
            db.session.query(User.id).filter(User.email == "john.doe@email.com").first()
        )
        review = RestaurantServices.review_restaurant(
            restaurant.id, reviewer.id, 5, "test"
        )
        assert review is not None

        db.session.query(Review).filter_by(id=review.id).delete()
        db.session.commit()

    def test_restaurant_name(self):
        """
        check the function that return the restaurant name
        """
        restaurant = (
            db.session.query(Restaurant)
            .filter(Restaurant.name == "Trial Restaurant")
            .first()
        )
        name = RestaurantServices.get_restaurant_name(restaurant.id)
        assert restaurant.name == name

    def test_three_reviews(self):
        """
        check the three reviews fetcher
        """

        restaurant = (
            db.session.query(Restaurant.id)
            .filter(Restaurant.name == "Trial Restaurant")
            .first()
        )
        reviewer = (
            db.session.query(User.id).filter(User.email == "john.doe@email.com").first()
        )
        review1 = RestaurantServices.review_restaurant(
            restaurant.id, reviewer.id, 5, "test1"
        )
        review2 = RestaurantServices.review_restaurant(
            restaurant.id, reviewer.id, 4, "test2"
        )
        review3 = RestaurantServices.review_restaurant(
            restaurant.id, reviewer.id, 3, "test3"
        )

        three_reviews = RestaurantServices.get_three_reviews(restaurant.id)
        assert three_reviews is not None
        assert len(three_reviews) == 3

        db.session.query(Review).filter_by(id=review1.id).delete()
        db.session.query(Review).filter_by(id=review2.id).delete()
        db.session.query(Review).filter_by(id=review3.id).delete()

        db.session.commit()

    def test_search_restaurant_by_key_ok_complete_name(self):
        """
        This test unit test the service to perform the search by keyword of the restaurants
        on persistence
        """
        rest_by_name = RestaurantServices.get_restaurants_by_keyword(name="Trial")
        assert len(rest_by_name) is 1

    def test_search_restaurant_by_key_ok_partial_name(self):
        """
        This test unit test the service to perform the search by keyword of the restaurants
        on persistence
        """
        user = create_user_on_db()
        rest = create_restaurants_on_db("Gino Sorbillo", user.id)
        assert rest is not None
        rest_by_name = RestaurantServices.get_restaurants_by_keyword(name=rest.name)
        assert len(rest_by_name) is 1

        rest_by_name = RestaurantServices.get_restaurants_by_keyword(name="Gino")
        assert len(rest_by_name) is 1

        rest_by_name = RestaurantServices.get_restaurants_by_keyword(name="gino")
        assert len(rest_by_name) is 1

        rest_by_name = RestaurantServices.get_restaurants_by_keyword(name="Sorbillo")
        assert len(rest_by_name) is 1

        rest_by_name = RestaurantServices.get_restaurants_by_keyword(name="sorbillo")
        assert len(rest_by_name) is 1

        del_user_on_db(user.id)
        for rest in rest_by_name:
            del_restaurant_on_db(rest.id)

    def test_delete_dish_menu(self, client):
        """
        check if dish get deletedS
        """
        email = "ham.burger@email.com"
        password = "operator"
        response = login(client, email, password)
        assert response.status_code == 200
        assert "logged_test" in response.data.decode("utf-8")

        dish = MenuDish()
        dish.name = "Pearà"
        dish.price = 5.50
        dish.restaurant_id = 1
        db.session.add(dish)
        db.session.commit()
        assert dish is not None

        client.get("/restaurant/menu/delete/" + str(dish.id))

        dish = db.session.query(MenuDish).filter_by(name="Pearà").first()
        assert dish is None

    def test_checkin_reservation(self):
        """
        test mark checked in a reservation by operator
        """
        reservation = db.session.query(Reservation).first()
        reservation_query = db.session.query(Reservation).filter_by(id=reservation.id)
        reservation_query.update({Reservation.checkin: False})
        RestaurantServices.checkin_reservations(reservation.id)
        assert reservation.checkin is True
        reservation_query = db.session.query(Reservation).filter_by(id=reservation.id)
        reservation_query.update({Reservation.checkin: False})
        db.session.commit()
        db.session.flush()
