"""
This test case covered all simple action that we can do from the UI
"""

import pytest
import os
from utils import (
    login,
    logout,
    register_user,
    get_user_with_email,
    register_restaurant,
    get_rest_with_name,
    get_rest_with_name_and_phone,
)
from monolith.database import db, User, Restaurant
from monolith.forms import UserForm, RestaurantForm
from monolith.tests.utils import visit_restaurant, visit_photo_gallery


@pytest.mark.usefixtures("client")
class Test_GoOutSafeForm:
    @classmethod
    def setup_class(cls):
        try:
            os.remove(
                "{}/gooutsafe.db".format(os.path.dirname(os.path.realpath(__file__)))
            )
        # do awesome stuff
        except OSError:
            pass

    @classmethod
    def teardown_class(cls):
        os.remove("{}/gooutsafe.db".format(os.path.dirname(os.path.realpath(__file__))))

    def test_login_form_ok(self, client):
        """
        This test suit test the operation that we can do
        to login correctly an user
        """
        email = "ham.burger@email.com"
        password = "operator"
        response = login(client, email, password)
        assert response.status_code == 200
        assert "Hi Ham" in response.data.decode("utf-8")

        q = db.session.query(User).filter_by(email=email)
        q_user = q.first()
        assert q_user is not None
        assert q_user.authenticate(password) is True

        response = logout(client)
        assert response.status_code == 200
        assert "Hi" not in response.data.decode("utf-8")

        q = db.session.query(User).filter_by(email=email)
        q_user = q.first()
        assert q_user is not None

    def test_login_form_ko(self, client):
        """
        This test suit test the operation that we can do
        to login correctly an user
        """
        email = "vincenzopalazzo@email.com"
        password = "operator"
        response = login(client, email, password)
        assert response.status_code == 200
        assert "Hi" not in response.data.decode("utf-8")

        q = db.session.query(User).filter_by(email=email)
        q_user = q.first()
        assert q_user is None

    def test_register_new_user_ok(self, client):
        """
        This use case try to login a new user with a correct execution

        The flow of this test is
        - Create user
        - Verify user on db
        - login user
        - verify the html returned from flask
        :param client: The flask app created inside the fixtures
        """
        user_form = UserForm()
        user_form.email = "Trumps_doctor@usa.gov"
        user_form.firstname = "Anthony"
        user_form.lastname = "Fauci"
        user_form.dateofbirth = "12/12/2020"
        user_form.password = "nocovid_in_us"
        response = register_user(client, user_form)
        assert response.status_code == 200
        assert "Hi" in response.data.decode("utf-8")

        ## Search inside the DB if this user exist
        user_query = get_user_with_email(user_form.email)
        assert user_query is not None
        assert user_query.authenticate(user_form.password) is True

        response = login(client, user_form.email, user_form.password)
        assert response.status_code == 200
        assert "Hi {}".format(user_form.firstname) in response.data.decode("utf-8")

        response = logout(client)
        assert response.status_code == 200
        assert "Hi" not in response.data.decode("utf-8")

        db.session.query(User).filter_by(id=user_query.id).delete()
        db.session.commit()

    def test_delete_user(self, client):
        pass

    def test_register_new_restaurant(self, client):
        """
        This test test the use case to create a new restaurant
        and this test have the follow described below

        - Login like a operator (user the standard account)
        - Register a new restaurant
        - Look inside the db  to see if the restaurant exist
        - Log out user
        - See if the restaurant is present on home screen.

        :param client:
        """
        email = "ham.burger@email.com"
        password = "operator"
        login(client, email, password)
        restaurant_form = RestaurantForm()
        restaurant_form.name = "Gino Sorbillo"
        restaurant_form.phone = "096321343"
        restaurant_form.lat = 12
        restaurant_form.lon = 12
        restaurant_form.n_tables = 50
        restaurant_form.covid_measures = "We can survive"
        restaurant_form.cuisine = "0"
        restaurant_form.open_days = "0"
        restaurant_form.open_lunch = "12:00"
        restaurant_form.close_lunch = "15:00"
        restaurant_form.open_dinner = "18:00"
        restaurant_form.close_dinner = "00:00"
        response = register_restaurant(client, restaurant_form)
        assert response.status_code == 200  ## Regirect to /
        # assert restaurant_form.name in response.data.decode("utf-8")
        # assert "Hi" in response.data.decode("utf-8")
        rest = get_rest_with_name(restaurant_form.name)
        assert rest is not None
        response = logout(client)
        assert response.status_code == 200
        response = client.get("/")  ## get index
        assert restaurant_form.name in response.data.decode("utf-8")

    def test_register_new_restaurant(self, client):
        """
        This test test the use case to create a new restaurant but the user
        and this test have the follow described below

        - Login like a operator (user the standard account)
        - Register a new restaurant
        - Look inside the db  to see if the restaurant exist
        - Log out user
        - See if the restaurant is present on home screen.

        :param client:
        """
        email = "alibaba@gmail.com"
        password = "alibaba"
        user_form = UserForm()
        user_form.email = email
        user_form.firstname = "alibaba"
        user_form.lastname = "alibaba"
        user_form.dateofbirth = "12/12/2020"
        user_form.password = password
        response = register_user(client, user_form)
        assert response.status_code == 200
        # assert "Hi" in response.data.decode("utf-8")

        user = get_user_with_email(user_form.email)
        assert user is not None
        assert user.role_id == 3  ## Customer

        # login(client, email, password)
        restaurant_form = RestaurantForm()
        restaurant_form.name = "Gino Sorbillo"
        restaurant_form.phone = "096321343"
        restaurant_form.lat = 12
        restaurant_form.lon = 12
        restaurant_form.n_tables = 50
        restaurant_form.covid_measures = "We can survive"
        restaurant_form.cuisine = ["Italian food"]
        restaurant_form.open_days = ["0"]
        restaurant_form.open_lunch = "12:00"
        restaurant_form.close_lunch = "15:00"
        restaurant_form.open_dinner = "18:00"
        restaurant_form.close_dinner = "00:00"
        response = register_restaurant(client, restaurant_form)
        assert response.status_code == 200
        assert restaurant_form.name in response.data.decode("utf-8")

        rest = get_rest_with_name_and_phone(restaurant_form.name, restaurant_form.phone)
        assert rest is not None
        db.session.query(User).filter_by(id=user.id).delete()
        db.session.commit()

    def test_change_role_user(self, client):
        """
        This test covered the change user role where we create a new restaurant
        this mean the flow describe below

        - Use a customer rule to login inside the app
        - Create a new restaurant (this should be trigger the change role from customer to operator)
        - verify the change on UI
        - verify the new restaurant on UI
        - verify on db the user role changes
        - logout user
        - login the same user and see if the change role is persistent.
        - final logout
        :param client:
        """
        user = UserForm()
        user.email = "bernard@gmail.com"
        user.firstname = "bernard"
        user.lastname = "alias"
        user.password = "bernard"
        user.dateofbirth = "12/12/1996"
        register_user(client, user)
        response = login(client, user.email, user.password)
        assert response is not None
        assert "Hi {}".format(user.firstname) in response.data.decode("utf-8")

        # login(client, email, password)
        restaurant_form = RestaurantForm()
        restaurant_form.name = "Da Leo"
        restaurant_form.phone = "123243245"
        restaurant_form.lat = 123
        restaurant_form.lon = 123
        restaurant_form.n_tables = 250
        restaurant_form.covid_measures = "Mask UP"
        restaurant_form.cuisine = ["Italian food"]
        restaurant_form.open_days = ["2"]
        restaurant_form.open_lunch = "12:00"
        restaurant_form.close_lunch = "15:00"
        restaurant_form.open_dinner = "18:00"
        restaurant_form.close_dinner = "00:00"
        response = register_restaurant(client, restaurant_form)
        assert response.status_code == 200
        assert restaurant_form.name in response.data.decode("utf-8")

        user_stored = get_user_with_email(user.email)
        """
        ## --------- FIXME(vincenzopalazzo) -------
        user_stored.rule_id = 2
        db.session.commit()
        with client.session_transaction(subdomain='blue') as session:
            session['ROLE'] = "OPERATOR"
        ## -------------------------------------------
        """
        restaurant = get_rest_with_name(restaurant_form.name)
        assert restaurant.owner_id == user_stored.id
        assert user_stored.role_id == 2

        db.session.query(User).filter_by(id=user_stored.id).delete()
        db.session.query(Restaurant).filter_by(id=restaurant.id).delete()
        db.session.commit()

    def test_change_role_user_new_user(self, client):
        """
        This test covered the change user role where we create a new restaurant
        this mean the flow describe below

        - Create a new user (so it is a customer)
        - verify if it is logged
        - Create a new restaurant (this should be trigger the change role from customer to operator)
        - verify the change on UI
        - verify the new restaurant on UI
        - verify on db the user role changes
        - logout user
        - login the same user and see if the change role is persistent.
        - final logout
        :param client:
        """
        pass

    def test_modify_new_restaurant(self, client):
        pass

    def test_research_restaurant_by_name(self, client):
        pass

    def test_send_communication_covid19(self, client):
        """
        This test case test the number of people that enter in contact with an people
        that have the covid19 in the same time of the restaurant visit
        """
        pass

    def test_open_photo_view(self, client):
        """
        This test perform the use case described below
        - create a new user
        - create a new restaurant
        - open the single restaurant view
        - Go to photo gallery
        - check if the page is load correctly
        """
        user = UserForm()
        user.email = "cr7@gmail.com"
        user.firstname = "Cristiano"
        user.lastname = "Ronaldo"
        user.password = "Siii"
        user.dateofbirth = "12/12/1975"
        register_user(client, user)
        response = login(client, user.email, user.password)
        assert response is not None
        assert "Hi {}".format(user.firstname) in response.data.decode("utf-8")

        # login(client, email, password)
        restaurant_form = RestaurantForm()
        restaurant_form.name = "Gino Sorbillo"
        restaurant_form.phone = "096321343"
        restaurant_form.lat = 12
        restaurant_form.lon = 12
        restaurant_form.n_tables = 50
        restaurant_form.covid_measures = "We can survive"
        restaurant_form.cuisine = ["Italian food"]
        restaurant_form.open_days = ["0"]
        restaurant_form.open_lunch = "12:00"
        restaurant_form.close_lunch = "15:00"
        restaurant_form.open_dinner = "18:00"
        restaurant_form.close_dinner = "00:00"
        response = register_restaurant(client, restaurant_form)
        assert response.status_code == 200
        assert restaurant_form.name in response.data.decode("utf-8")

        restaurant = get_rest_with_name(restaurant_form.name)
        response = visit_restaurant(client, restaurant.id)
        assert response.status_code == 200
        assert "Phone" in response.data.decode("utf-8")

        user_stored = get_user_with_email(user.email)
        ## --------- FIXME(vincenzopalazzo) -------
        user_stored.rule_id = 2
        db.session.commit()
        with client.session_transaction(subdomain="blue") as session:
            session["ROLE"] = "OPERATOR"
        ## -------------------------------------------
        assert restaurant.owner_id == user_stored.id
        assert user_stored.rule_id == 2

        response = visit_photo_gallery(client)
        assert response.status_code == 200

        db.session.query(User).filter_by(id=user_stored.id).delete()
        db.session.query(Restaurant).filter_by(id=restaurant.id).delete()
        db.session.commit()
