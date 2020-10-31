from flask import Blueprint, render_template, session
from flask_login import current_user

from monolith.database import db, Restaurant, Positive
from monolith.forms import ReservationForm
from monolith.services import UserService

home = Blueprint("home", __name__)


@home.route("/")
def index():
    restaurants = db.session.query(Restaurant).all()
    if current_user is None:
        _test = "anonymous_test"
    else:
        _test = "logged_test"
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
                _test=_test,
                n_positive=n_positive,
                n_healed=n_healed,
            )
        elif session["ROLE"] == "OPERATOR":
            return render_template(
                "index_operator.html", _test=_test, restaurants=restaurants
            )
        elif session["ROLE"] == "CUSTOMER":
            form = ReservationForm()
            is_positive = UserService.is_positive(current_user.id)
            return render_template(
                "index_customer.html",
                _test=_test,
                restaurants=restaurants,
                form=form,
                is_positive=is_positive,
            )

    return render_template("index.html", _test=_test, restaurants=restaurants)
