import pytest
from monolith.database import db, User, Restaurant
from monolith.forms import UserForm, RestaurantForm
from monolith.services.restaurant_services import RestaurantServices
from datetime import datetime, time

@pytest.mark.usefixtures("client")
class Test_RestaurantServices:
    """"""

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
        form.open_lunch.data = datetime.time(datetime(2020, 7, 1))
        form.close_lunch.data = datetime.time(datetime(2020, 7, 1))
        form.open_dinner.data = datetime.time(datetime(2020, 7, 1))
        form.close_dinner.data = datetime.time(datetime(2020, 6, 1))
        q_user = db.session.query(User).filter_by(email="ham.burger@email.com").first()
        restaurant = RestaurantServices.create_new_restaurant(form, q_user.id, 6)
        assert restaurant is not None

        db.session.query(Restaurant).filter_by(id=restaurant.id).delete()
        db.session.commit()
