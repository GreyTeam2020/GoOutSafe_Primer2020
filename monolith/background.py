import time
from decimal import Decimal

from celery import Celery
from monolith.utils import *
from monolith.database import db, Restaurant, Review
from monolith.services import RestaurantServices

## redis inside the http is the name of network that is called like the containser
## a good reference is https://stackoverflow.com/a/55410571/7290562
from monolith.utils import (
    send_positive_in_restaurant,
    send_positive_booking_in_restaurant,
)

celery = Celery()
_APP = None

@celery.task()
def send_email_to_confirm_registration(to_email: str, to_name: str, with_toke: str):
    """
    Perform the celery task to send the email registration
    it take the following element
    :param to_email: Email to send the message
    :param to_name: The user name to send the message
    :param with_toke: The token of user on system
    """
    send_registration_confirm(to_email, to_name, with_toke)


@celery.task()
def send_alert_new_covid19_about_previous_booking(
    to_email: str, to_name: str, email_user: str, restaurant_name: str
):
    """
    Perform the send email with celery async task to send a email to all restaurants with a booking from the person
    positive to covid19.
    :param to_email:
    :param to_name:
    :param email_user:
    :param restaurant_name:
    :return:
    """
    send_positive_booking_in_restaurant(to_email, to_name, email_user, restaurant_name)


@celery.task()
def send_positive_in_restaurant_celery(
    to_email: str, to_name: str, date_possible_contact: str, restaurant_name: str
):
    """
    Perform the send email with celery async task to send an email to the restaurant where a new positive cases was
    """
    send_positive_in_restaurant(
        to_email, to_name, date_possible_contact, restaurant_name
    )


@celery.task()
def send_possible_positive_contact_to_friend_celery(
    to_email: str, date_possible_contact: str, restaurant_name: str
):
    """
    Perform the send email with celery async task to send an email to friends with a reservation
    :param to_email:
    :param date_possible_contact:
    :param restaurant_name:
    """
    send_possible_positive_contact_to_friend(
        to_email, date_possible_contact, restaurant_name
    )


@celery.task()
def send_possible_positive_contact_celery(
    to_email: str, to_name: str, date_possible_contact: str, restaurant_name: str
):
    """
    Perform the send email with celery async task to send an email to the customer in a restaurants where a new positive
    case was
    :param to_email:
    :param to_name:
    :param date_possible_contact:
    :param restaurant_name:
    """
    send_possible_positive_contact(
        to_email, to_name, date_possible_contact, restaurant_name
    )

@celery.task()
def send_booking_confirmation_to_friends_celery(to_email: str, to_name: str, to_restaurants: str, to_friend_list: [], date_time):
    """

    :param to_email:
    :param to_name:
    :param to_restaurants:
    :param to_friend_list:
    :param date_time:
    :return:
    """
    send_booking_confirmation_to_friends(to_email, to_name, to_restaurants, to_friend_list, date_time)

@celery.task
def calculate_rating_on_background():
    """
    This task make a calculation of review rating inside each
    this task take the db code and call the RestaurantServices for each restaurants
    """
    # Calls RestaurantServices.calculate_rating_for_all() every 30 seconds
    with _APP.app_context():
        RestaurantServices.calculate_rating_for_all()

def init_celery(app, worker=False):
    global _APP

    # Load Celery with mock app
    celery.config_from_object(app.config)
    _APP = app