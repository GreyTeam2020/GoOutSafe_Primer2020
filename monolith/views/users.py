from flask import Blueprint, redirect, render_template, request
from monolith.database import db, User
from monolith.auth import admin_required
from monolith.forms import UserForm
from monolith.utils import SendMail

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
            new_user = User()
            form.populate_obj(new_user)
            new_user.set_password(
                form.password.data
            )  # pw should be hashed with some salt
            db.session.add(new_user)
            db.session.commit()
            return redirect("/users")

    return render_template("create_user.html", form=form)


@users.route("/testsendemail")
def _testsendemail():
    # ------------------------
    testEmail = 'PUTYOUREMAIL'  # PUT YOUR EMAIL FOR TEST and click to /login
    SendMail.sendPossibilePositiveContact(testEmail, 'John Doe', '01/01/2020 21:30', 'Il Paninaro')
    SendMail.sendReservationConfirm(testEmail, 'John Doe', '01/01/2020 21:30', 'Il Paninaro', 10)
    SendMail.sendRegistrationConfirm(testEmail, 'John Doe', 'qwertyuiopasdfghjklzxcvbnm')
    SendMail.sendReservationNotification(testEmail, 'John Doe', 'Il Paninaro', 'Richard Smith', '01/01/2020 21:30', 12, 8)
    # ------------------------
    return render_template("sendemailok.html", testEmail=testEmail)