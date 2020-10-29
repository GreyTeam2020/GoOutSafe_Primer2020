import pytest
from monolith.database import db, User, Restaurant
from monolith.forms import RestaurantForm
from monolith.services.restaurant_services import RestaurantServices
from datetime import datetime


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