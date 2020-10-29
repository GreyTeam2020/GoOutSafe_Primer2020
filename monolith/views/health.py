from flask import Blueprint, redirect, render_template, request

from monolith.auth import roles_allowed
from monolith.database import db, User
from monolith.forms import SearchUserForm
from monolith.services import HealthyServices, RestaurantServices

health = Blueprint("health", __name__)


@health.route("/allrestaurants")
def allrestaurants():
    restaurants = RestaurantServices.get_all_restaurants()
    return render_template("all_restaurants.html", restaurants=restaurants)


@health.route("/report_positive")
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
