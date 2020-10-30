import json
from monolith.database import db, User, Restaurant, Positive
from monolith.forms import UserForm, RestaurantForm, SearchUserForm, ReviewForm
from monolith.services import UserService


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
    :return: response from URL "/user/create_user"
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
    return client.post("/user/create_user", data=data, follow_redirects=True)


def register_restaurant(client, restaurant: RestaurantForm):
    """
    This method perform the request  to build a new restaurant
    :param client: Is a flask app created inside the fixtures
    :param restaurant: Is the restaurant form populate with the mock data
    :return: response from URL "/create_restaurant"
    """
    return client.post(
        "/restaurant/create",
        data=dict(
            name=restaurant.name,
            phone=restaurant.phone,
            lat=restaurant.lat,
            lon=restaurant.lon,
            n_tables=restaurant.n_tables,
            covid_measures=restaurant.covid_measures,
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


def mark_people_for_covid19(client, form: SearchUserForm):
    """
    This method perform the request to mark a people as positive
    :return: response from request
    """
    return client.post(
        "/mark_positive",
        data=dict(
            email=form.email,
            phone=form.phone,
            submit=True,
            headers={"Content-type": "application/x-www-form-urlencoded"},
        ),
        follow_redirects=True,
    )


def visit_restaurant(client, restaurant_id):
    """
    This perform the request to visit the restaurant view
    :param client:
    :param restaurant_id:
    :return: response from client
    """
    return client.get("/restaurant/{}".format(restaurant_id), follow_redirects=True)


def visit_photo_gallery(client):
    """
    This perform the request to visit the photo_gallery view
    :param client:
    :param restaurant_id:
    :return: response from client
    """
    return client.get("/restaurant/photogallery", follow_redirects=True)


def visit_reservation(client, from_date, to_date, email):
    """
    This perform the URL to visit the reservatioin of a restaurants
    ----- This is an example of URL --
    http://localhost:5000/list_reservations?fromDate=2013-10-07&toDate=2014-10-07&email=john.doe@email.com
    """
    return client.get(
        "/restaurant/reservations?fromDate={}&toDate={}&email={}".format(
            from_date, to_date, email
        ),
        follow_redirects=True,
    )


def make_revew(client, restaurant_id: int, form: ReviewForm):
    """
    perform the flask request to make a new url
    """
    return client.post(
        "/restaurant/review/{}".format(restaurant_id),
        data=dict(
            stars=form.stars,
            review=form.review,
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


def get_rest_with_name_and_phone(name, phone):
    """
    This method factorize the code to get an restaurant with a name
    :param name: the email that we want use to query the user
    :return: return the user if exist otherwise None
    """
    q = db.session.query(Restaurant).filter_by(name=name, phone=phone)
    q_rest = q.first()
    if q_rest is not None:
        return q_rest
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


def create_user_on_db():
    form = UserForm()
    form.data["email"] = "alibaba@alibaba.com"
    form.data["password"] = "Alibaba"
    form.firstname = "Vincenzo"
    form.lastname = "Palazzo"
    form.password = "Alibaba"
    form.phone = "12345"
    form.dateofbirth = "12/12/2020"
    form.email.data = "alibaba@alibaba.com"
    user = User()
    form.populate_obj(user)
    return UserService.create_user(user, form.password)


def del_user_on_db(id):
    db.session.query(User).filter_by(id=id).delete()
    db.session.commit()


def positive_with_user_id(user_id: int = None, marked: bool = True):
    """
    This method is an util function to search inside the positive user
    """
    if user_id is None:
        return db.session.query(Positive).all()
    else:
        return (
            db.session.query(Positive).filter_by(user_id=user_id, marked=marked).first()
        )


def delete_positive_with_user_id(user_id: int, marked: bool = True):
    """
    This method is an util function to search inside the positive user
    """
    return db.session.query(Positive).filter_by(user_id=user_id, marked=marked).delete()


def delete_was_positive_with_user_id(user_id: int, marked: bool = True):
    """
    This delete a row of a previous positive person
    """
    return db.session.query(Positive).filter_by(user_id=user_id).delete()


def unmark_people_for_covid19(client, form: SearchUserForm):
    """
    This method perform the request to mark a people as not positive
    :return: response from request
    """
    return client.post(
        "/unmark_positive",
        data=dict(
            email=form.email,
            phone=form.phone,
            submit=True,
            headers={"Content-type": "application/x-www-form-urlencoded"},
        ),
        follow_redirects=True,
    )


def search_contact_positive_covid19(client, form: SearchUserForm):
    """
    This method search contacts with a covid19 positive person
    """
    return client.post(
        "/search_contacts",
        data=dict(
            email=form.email,
            phone=form.phone,
            submit=True,
            headers={"Content-type": "application/x-www-form-urlencoded"},
        ),
        follow_redirects=True,
    )
