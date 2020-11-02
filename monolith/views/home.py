from flask import Blueprint, render_template, session, redirect
from flask_login import current_user

from monolith.database import (
    db,
    Restaurant,
    Positive,
    OpeningHours,
    Menu,
    PhotoGallery,
    MenuDish,
)
from monolith.forms import ReservationForm
from monolith.services import UserService, RestaurantServices

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
            if "RESTAURANT_ID" in session:
                restaurant_id = session["RESTAURANT_ID"]
                record = (
                    db.session.query(Restaurant)
                    .filter_by(id=int(restaurant_id))
                    .first()
                )
                weekDaysLabel = [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ]
                q_hours = (
                    db.session.query(OpeningHours)
                    .filter_by(restaurant_id=int(restaurant_id))
                    .all()
                )
                q_cuisine = (
                    db.session.query(Menu)
                    .filter_by(restaurant_id=int(restaurant_id))
                    .all()
                )
                photos = PhotoGallery.query.filter_by(
                    restaurant_id=int(restaurant_id)
                ).all()
                dishes = (
                    db.session.query(MenuDish)
                    .filter_by(restaurant_id=restaurant_id)
                    .all()
                )

                return render_template(
                    "restaurantsheet.html",
                    id=restaurant_id,
                    name=record.name,
                    lat=record.lat,
                    lon=record.lon,
                    phone=record.phone,
                    covid_measures=record.covid_measures,
                    hours=q_hours,
                    cuisine=q_cuisine,
                    weekDaysLabel=weekDaysLabel,
                    photos=photos,
                    reviews=RestaurantServices.get_three_reviews(restaurant_id),
                    dishes=dishes,
                    _test=_test,
                )
            else:
                return render_template("norestaurant.html", _test=_test)
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
