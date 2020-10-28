from flask import Blueprint, redirect, render_template, request
from monolith.database import db, Restaurant, User, Positive
from monolith.forms import SearchUser
from datetime import datetime

health = Blueprint("health", __name__)


@health.route("/allrestaurants")
def allrestaurants():
    restaurants = db.session.query(Restaurant)
    return render_template("all_restaurants.html", restaurants=restaurants)


@health.route("/report_positive")
def report_positive():
    users = db.session.query(User)
    return render_template("report_positive.html", users=users)


@health.route("/mark_positive", methods=["POST", "GET"])
def mark_positive():
    form = SearchUser()
    if request.method == "POST":
        if form.validate_on_submit():

            if form.email.data == "" and form.phone.data == "":
                return render_template(
                    "mark_positive.html",
                    form=form,
                    message="Insert an email or a phone number".format(form.email.data),
                )

            # filtering by email
            if form.email.data != "":
                q_user = db.session.query(User).filter_by(email=form.email.data)
            else:
                q_user = db.session.query(User).filter_by(phone=form.phone.data)

            if q_user.first() is None:
                return render_template(
                    "mark_positive.html",
                    form=form,
                    message="The user is not registered".format(form.email.data),
                )

            # settare l'utente q_user come positivo
            q_already_positive = (
                db.session.query(Positive)
                .filter_by(user_id=q_user.first().id, marked=True)
                .first()
            )
            if q_already_positive is None:
                # non è già stato marcato come positivo, inserisco una nuova riga nella tabella

                new_positive = Positive()
                new_positive.from_date = datetime.today()
                new_positive.marked = True
                new_positive.user_id = q_user.first().id

                db.session.add(new_positive)
                db.session.commit()

            else:
                return render_template(
                    "mark_positive.html",
                    form=form,
                    message="User with email {} already Covid-19 positive".format(
                        form.email.data
                    ),
                )

            return redirect("/")
    return render_template("mark_positive.html", form=form)
