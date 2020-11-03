from flask import Flask
from flask_mail import Mail, Message
import os

# Methods and configuration for send email
app = Flask(__name__)
app.config.from_pyfile(os.path.join("..", "config/app.config"), silent=False)

# EMAIL CONFIG
app.config["MAIL_SERVER"] = app.config.get("MAIL_SERVER")
app.config["MAIL_PORT"] = app.config.get("MAIL_PORT")
app.config["MAIL_USERNAME"] = app.config.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = app.config.get("MAIL_PASSWORD")
app.config["MAIL_USE_TLS"] = app.config.get("MAIL_USE_TLS")
app.config["MAIL_USE_SSL"] = app.config.get("MAIL_USE_SSL")
mail = Mail(app)


def send_possible_positive_contact(
    to_email, to_name, date_possible_contact, restaurant_name
):
    """
    Compose positive COVID-19 contact notification email template and sends to customer
    """
    subject = "Possible COVID-19 contact"
    body = (
        "Hi {toName},<br>"
        'you had a possible COVID-19 contact at restaurant "{restaurantName}" in date {datePossibleContact}.<br> '
        "<br>Please contact authority at 911 and follow regulations at the following link:<br> "
        "http://www.salute.gov.it/portale/nuovocoronavirus/homeNuovoCoronavirus.jsp<br> "
    )
    body = body.replace("{toName}", to_name)
    body = body.replace("{restaurantName}", restaurant_name)
    body = body.replace("{datePossibleContact}", date_possible_contact)
    send_email(subject, body, to_email)


def send_reservation_confirm(
    to_email, to_name, date_reservation, restaurant_name, number_seat
):
    """
    Compose reservation confirm email template and sends to customer
    """
    subject = "Reservation confirmed"
    body = (
        "Hi {toName},<br>"
        "we are glad to confirm your table for {numberSeat} people "
        'at restaurant "{restaurantName}" in date {dateReservation}<br> '
        "<br>See you soon!<br> "
    )
    body = body.replace("{toName}", to_name)
    body = body.replace("{restaurantName}", restaurant_name)
    body = body.replace("{dateReservation}", date_reservation)
    body = body.replace("{numberSeat}", str(number_seat))
    send_email(subject, body, to_email)


def send_reservation_notification(
    to_email,
    to_name,
    restaurant_name,
    customer_name,
    date_reservation,
    table_number,
    number_seat,
):
    """
    Compose reservation notification email template and sends to operator
    """
    subject = "Reservation notification"
    body = (
        "Hi {toName} from {restaurantName},<br>"
        "you have a new reservation:<br>"
        "<ul>"
        "<li>customer name: {customerName}</li>"
        "<li>number of seats: {numberSeat}</li>"
        "<li>date: {dateReservation}</li>"
        "<li>table number: {tableNumber}</li>"
        "</ul>"
        "See you soon! "
    )
    body = body.replace("{toName}", to_name)
    body = body.replace("{restaurantName}", restaurant_name)
    body = body.replace("{customerName}", customer_name)
    #body = body.replace("{numberSeat}", str(numberSeat))
    body = body.replace("{dateReservation}", date_reservation)
    body = body.replace("{tableNumber}", str(table_number))
    send_email(subject, body, number_seat)


def send_registration_confirm(to_email, to_name, token):
    """
    Compose registration confirm email template and sends to user
    """
    subject = "Confirm email"
    body = (
        "Hi {toName},<br>"
        "we are glad to have you in GoOutSafe but you must confirm your email"
        'by click on <a href="http://localhost:5000/confirme_mail?token={token}">this URL<a>.<br>'
        "<br>See you soon! "
    )
    body = body.replace("{toName}", to_name)
    body = body.replace("{token}", token)
    send_email(subject, body, to_email)


def send_email(subject, body, recipient):
    """
    Internal method for send email
    """
    subject = "[GoOutSafe] " + subject
    msg = Message(
        recipients=[recipient],
        sender="greyteam2020@gmail.com",
        html=body,
        subject=subject,
    )
    mail.send(msg)
    return 0


def send_positive_booking_in_restaurant(to_email, to_name, email_user, restaurant_name):
    """
    A positive COVID-19 booked in a restaurant
    """
    subject = "A COVID-19 positive person has a booking in your restaurant"
    body = (
        "Hi {toName},<br>"
        'we inform you that the user with email {emalUser}, who is Covid19 positive, has a booking in your restaurant "{restaurantName}"<br>'
    )
    body = body.replace("{toName}", to_name)
    body = body.replace("{restaurantName}", restaurant_name)
    body = body.replace("{emalUser}", email_user)
    send_email(subject, body, to_email)


def send_possible_positive_contact_to_friend(
    to_email, date_possible_contact, restaurant_name
):
    """
    Compose positive COVID-19 contact notification email template and sends to customer
    """
    subject = "Possible COVID-19 contact"
    body = (
        "Hi,<br>"
        'you had a possible COVID-19 contact at restaurant "{restaurantName}" in date {datePossibleContact}.<br> '
        "<br>Please contact authority at 911 and follow regulations at the following link:<br> "
        "http://www.salute.gov.it/portale/nuovocoronavirus/homeNuovoCoronavirus.jsp<br> "
    )
    body = body.replace("{restaurantName}", restaurant_name)
    body = body.replace("{datePossibleContact}", date_possible_contact)
    send_email(subject, body, to_email)