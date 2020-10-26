from flask import Blueprint, redirect, render_template, request, session
from monolith.database import db, Restaurant, User

health = Blueprint("health", __name__)


@health.route("/allrestaurants")
def allrestaurants():
    restaurants = db.session.query(Restaurant)
    return render_template("all_restaurants.html", restaurants=restaurants)


@health.route("/report_positive")
def report_positive():
    users = db.session.query(User)
    return render_template("report_positive.html", users=users)
