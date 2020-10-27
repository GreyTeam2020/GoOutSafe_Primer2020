import json
from monolith.database import db, User, Restaurant
from monolith.forms import UserForm, RestaurantForm


def login(client, username, password):
    return client.post(
        "/login",
        data=dict(
            email=username,
            password=password,
            submit=True,
            headers={"Content-type": "application/x-www-form-urlencoded"},
        ),
        follow_redirects=True,
    )


def logout(client):
    return client.get("/logout", follow_redirects=True)


def register_user(client, user: UserForm):
    """
    This method perform the request to register a new user
    :param client: Is a flask app created inside the fixtures
    :param user: Is the User form populate with the mock data
    :return: response from URL "/create_user"
    """
    data = dict(
        email=user.email,
        firstname=user.firstname,
        lastname=user.lastname,
        password=user.password,
        dateofbirth=user.dateofbirth,
        submit=True,
        headers={"Content-type": "application/x-www-form-urlencoded"},
    )
    return client.post(
        "/create_user",
        data=json.dumps(data),
        follow_redirects=True,
    )


def register_restaurant(client, restaurant: RestaurantForm, user_id=None):
    """
    This method perform the request  to build a new restaurant
    :param client: Is a flask app created inside the fixtures
    :param restaurant: Is the restaurant form populate with the mock data
    :return: response from URL "/create_restaurant"
    """
    return client.post(
        "/create_restaurant",
        data=dict(
            name=restaurant.name,
            phone=restaurant.phone,
            lat=restaurant.lat,
            lon=restaurant.lon,
            n_tables=restaurant.n_tables,
            covid_m=restaurant.covid_m,
            cuisine=restaurant.cuisine,
            open_days=restaurant.open_days,
            open_lunch=restaurant.open_lunch,
            close_lunch=restaurant.close_lunch,
            open_dinner=restaurant.open_dinner,
            close_dinner=restaurant.close_dinner,
            submit=True,
            headers={"Content-type": "application/x-www-form-urlencoded"},
        ),
        follow_redirects=True,
    )


def get_user_with_email(email):
    """
    This method factorize the code to get an user with a email
    :param email: the email that we want use to query the user
    :return: return the user if exist otherwise None
    """
    q = db.session.query(User).filter_by(email=email)
    q_user = q.first()
    if q_user is not None:
        return q_user
    return None


def get_rest_with_name(name):
    """
    This method factorize the code to get an restaurant with a name
    :param name: the email that we want use to query the user
    :return: return the user if exist otherwise None
    """
    q = db.session.query(Restaurant).filter_by(name=name)
    q_rest = q.first()
    if q_rest is not None:
        return q_rest
    return None
