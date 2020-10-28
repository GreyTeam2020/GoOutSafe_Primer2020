from flask import Blueprint, redirect, render_template, request, current_app, session
from monolith.database import db, User, Like, Role
from monolith.forms import UserForm
from monolith.utils import send_mail
from flask_login import login_user
from monolith.utils.dispaccer_events import DispatcherMessage
from monolith.app_constant import REGISTRATION_EMAIL
from monolith.services.user_service import UserService

users = Blueprint("users", __name__)


@users.route("/users")
def _users():
    users = db.session.query(User)
    return render_template("users.html", users=users)


@users.route("/create_user", methods=["GET", "POST"])
def create_user():
    form = UserForm()
    if request.method == "POST":
        if form.validate_on_submit():
            q = db.session.query(User).filter_by(email=form.email.data)
            if q.first() is not None:
                return render_template(
                    "create_user.html",
                    form=form,
                    message="Email {} already registered".format(form.email.data),
                )
            user = User()
            form.populate_obj(user)
            user = UserService.create_user(user, form.password.data)
            if user is not None and user.authenticate(form.password.data):
                login_user(user)
            DispatcherMessage.send_message(
                type_message=REGISTRATION_EMAIL,
                params=[user.email, user.lastname, "112344"],
            )
            newrole = db.session.query(Role).filter_by(id=user.role_id).first()
            if newrole is not None:
                session["ROLE"] = newrole.value

            return redirect("/")
    return render_template("create_user.html", form=form)


@users.route("/myreservations")
def myreservation():
    return render_template("user_reservations.html")


@users.route("/testsendemail")
def _testsendemail():
    # ------------------------
    testEmail = "PUTYOUREMAIL"  # PUT YOUR EMAIL FOR TEST and click to /login
    send_mail.sendPossibilePositiveContact(
        testEmail, "John Doe", "01/01/2020 21:30", "Il Paninaro"
    )
    send_mail.sendReservationConfirm(
        testEmail, "John Doe", "01/01/2020 21:30", "Il Paninaro", 10
    )
    send_mail.send_registration_confirm(
        testEmail, "John Doe", "qwertyuiopasdfghjklzxcvbnm"
    )
    send_mail.sendReservationNotification(
        testEmail, "John Doe", "Il Paninaro", "Richard Smith", "01/01/2020 21:30", 12, 8
    )
    # ------------------------
    return render_template("sendemailok.html", testEmail=testEmail)


@users.route("/testtpl")
def _testtpl():
    return render_template("testtpl.html")
