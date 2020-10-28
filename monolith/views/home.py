from flask import Blueprint, render_template

from monolith.database import db, Restaurant, Like
from monolith.auth import current_user
from monolith.forms import ReservationForm

home = Blueprint("home", __name__)


@home.route("/")
def index():
    restaurants = db.session.query(Restaurant)
    form = ReservationForm()
    return render_template("index.html", restaurants=restaurants, form=form)
