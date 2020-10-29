from flask import Blueprint, render_template, session

from monolith.database import db, Restaurant, Positive
from monolith.forms import ReservationForm

home = Blueprint("home", __name__)


@home.route("/")
def index():
    restaurants = db.session.query(Restaurant)

    if "ROLE" in session:
        if session["ROLE"] == "HEALTH":
            n_positive = db.session.query(Positive).filter_by(marked=True).count()
            n_healed = (
                db.session.query(Positive)
                    .filter_by(marked=False)
                    .distinct(Positive.user_id)
                    .count()
            )
            return render_template(
                "index_health.html",
                n_positive=n_positive,
                n_healed=n_healed,
            )
        elif session["ROLE"] == "OPERATOR":
            return render_template(
                "index_operator.html",
                restaurants=restaurants
            )
        elif session["ROLE"] == "CUSTOMER":
            form = ReservationForm()
            return render_template(
                "index_customer.html",
                restaurants=restaurants,
                form=form
            )

    return render_template(
        "index.html",
        restaurants=restaurants
    )
