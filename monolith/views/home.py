from flask import Blueprint, render_template

from monolith.database import db, Restaurant, Positive


home = Blueprint("home", __name__)


@home.route("/")
def index():
    restaurants = db.session.query(Restaurant)
    n_positive = db.session.query(Positive).filter_by(marked=True).count()
    n_healed = (
        db.session.query(Positive)
        .filter_by(marked=False)
        .distinct(Positive.user_id)
        .count()
    )

    return render_template(
        "index.html", restaurants=restaurants, n_positive=n_positive, n_healed=n_healed
    )
