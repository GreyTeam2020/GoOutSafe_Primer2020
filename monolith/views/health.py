from flask import Blueprint, redirect, render_template, request

from monolith.auth import roles_allowed
from monolith.database import db, User
from monolith.forms import SearchUserForm
from monolith.services import HealthyServices, RestaurantServices

health = Blueprint("health", __name__)


@health.route("/health/allrestaurants")
def allrestaurants():
    restaurants = RestaurantServices.get_all_restaurants()
    return render_template("all_restaurants.html", restaurants=restaurants)


@health.route("/health/report_positive")
def report_positive():
    users = db.session.query(User)
    return render_template("report_positive.html", users=users)


@health.route("/mark_positive", methods=["POST", "GET"])
@roles_allowed(roles=["HEALTH"])
def mark_positive():
    form = SearchUserForm()
    if request.method == "POST":
        if form.validate_on_submit():
            email = form.email.data
            phone = form.phone.data
            message = HealthyServices.mark_positive(email, phone)
            if message != "":
                return render_template("mark_positive.html", form=form, message=message)
            return redirect("/")
    return render_template("mark_positive.html", form=form)


@health.route("/search_contacts", methods=["POST", "GET"])
@roles_allowed(roles=["HEALTH"])
def search_contacts():

    form = SearchUserForm()
    if request.method == "POST":
        if form.validate_on_submit():

            if form.email.data=="" and form.phone.data=="":
                return render_template(
                    "search_contacts.html",
                    form=form,
                    message="Insert an email or a phone number".format(
                        form.email.data
                    ),
                )

            #filtering by email
            if form.email.data!="":
                q_user = db.session.query(User).filter_by(
                    email=form.email.data,
                )
            else:
                q_user = db.session.query(User).filter_by(
                    phone=form.phone.data,
                )

            if q_user.first() is None:
                return render_template(
                    "search_contacts.html",
                    form=form,
                    message="The user is not registered".format(
                        form.email.data
                    ),
                )

            q_already_positive = (
            db.session.query(Positive)
            .filter_by(user_id=q_user.first().id, marked=True)
            .first()
            )  
            if q_already_positive is None:
                return render_template(
                    "search_contacts.html",
                    form=form,
                    message="The user is not a covid-19 positive".format(
                        form.email.data
                    ),
                )
           

            contacts = HealthyServices.search_contacts(q_user.first().id)

            return render_template("/list_contacts.html", contacts=contacts)
    return render_template("/search_contacts.html", form=form)



@health.route("/unmark_positive", methods=["POST", "GET"])
@roles_allowed(roles=["HEALTH"])
def unmark_positive():
    form = SearchUserForm()
    if request.method == "POST":
        if form.validate_on_submit():
            email = form.email.data
            phone = form.phone.data
            message = HealthyServices.unmark_positive(email, phone)
            if message is None:
                return redirect("/")
            return render_template("unmark_positive.html", form=form, message=message)
    return render_template("unmark_positive.html", form=form)